import os

from dotenv import load_dotenv


load_dotenv()

TOKEN = os.getenv("TOKEN")
if not TOKEN or TOKEN == "PASTE_TELEGRAM_BOT_TOKEN_HERE":
    raise RuntimeError(
        "Укажите настоящий TOKEN в файле .env в корне проекта."
    )

try:
    ADMIN_USER_ID = int(os.getenv("ADMIN_USER_ID", "0"))
except ValueError as error:
    raise RuntimeError("ADMIN_USER_ID в .env должен быть целым числом.") from error

if ADMIN_USER_ID <= 0:
    raise RuntimeError("Укажите свой числовой ADMIN_USER_ID в файле .env.")

DB_FILE = os.getenv("DB_FILE", "finance_bot.db")
