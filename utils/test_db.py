import sqlite3

from configs.settings import DB_FILE


def check_connection():
    """Проверка подключения к основной базе данных SQLite."""
    try:
        with sqlite3.connect(DB_FILE) as connection:
            current_time = connection.execute(
                "SELECT CURRENT_TIMESTAMP"
            ).fetchone()[0]
        print(f"Подключение к SQLite успешно. Текущее время: {current_time}")
        return True
    except sqlite3.Error as error:
        print(f"Ошибка подключения к SQLite: {error}")
        return False


if __name__ == "__main__":
    check_connection()
