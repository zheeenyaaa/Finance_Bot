import logging


logger = logging.getLogger("telegram_bot")

# Одна централизованная настройка отключает все логи проекта.
logger.disabled = True
