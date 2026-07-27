import sqlite3

from bot_logging import logger
from configs.settings import DB_FILE


def connect_db():
    """Соединение с основной базой данных SQLite."""
    return sqlite3.connect(DB_FILE)


def get_total_users_count():
    """Получение общего количества пользователей."""
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM users")
        return cursor.fetchone()[0]
    except Exception as e:
        logger.error(
            "Ошибка при получении общего количества пользователей: %s",
            str(e),
        )
        return 0
    finally:
        cursor.close()
        conn.close()


def get_new_users_today():
    """Получение количества пользователей, зарегистрированных сегодня."""
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT COUNT(*) FROM users
            WHERE DATE(created_at) = DATE('now', 'localtime')
            """
        )
        return cursor.fetchone()[0]
    except Exception as e:
        logger.error(
            "Ошибка при получении новых пользователей: %s",
            str(e),
        )
        return 0
    finally:
        cursor.close()
        conn.close()


def get_admin_ids():
    """Получение списка ID администраторов."""
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT admin_id FROM admins")
        return [admin[0] for admin in cursor.fetchall()]
    except Exception as e:
        logger.error(
            "Ошибка при получении списка администраторов: %s",
            str(e),
        )
        return []
    finally:
        cursor.close()
        conn.close()


def is_admin(user_id):
    """Проверка, является ли пользователь администратором."""
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT 1 FROM admins WHERE admin_id = ?",
            (user_id,),
        )
        return cursor.fetchone() is not None
    except Exception as e:
        logger.error(
            "Ошибка при проверке прав администратора: %s",
            str(e),
        )
        return False
    finally:
        cursor.close()
        conn.close()


def add_admin(admin_id, username):
    """Добавление нового администратора."""
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT OR IGNORE INTO admins (admin_id, username)
            VALUES (?, ?)
            """,
            (admin_id, username),
        )
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        logger.error(
            "Ошибка при добавлении администратора: %s",
            str(e),
        )
        return False
    finally:
        cursor.close()
        conn.close()


def init_first_admin(admin_id):
    """Инициализация первого администратора при запуске."""
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM admins")
        if cursor.fetchone()[0] == 0:
            cursor.execute(
                """
                INSERT INTO admins (admin_id, username)
                VALUES (?, 'First Admin')
                """,
                (admin_id,),
            )
            conn.commit()
            return True
        return False
    except Exception as e:
        conn.rollback()
        logger.error(
            "Ошибка при инициализации первого администратора: %s",
            str(e),
        )
        return False
    finally:
        cursor.close()
        conn.close()
