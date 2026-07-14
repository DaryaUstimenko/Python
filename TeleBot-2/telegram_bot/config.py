import os
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env
load_dotenv()

# Загружаем токен бота из переменных окружения
BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    raise Exception('BOT_TOKEN не установлен в переменных окружения')

# ID администратора бота
ADMIN_ID = os.getenv('ADMIN_ID')

# Базовые настройки бота
WEBHOOK_URL = os.getenv('WEBHOOK_URL', '')  # URL для вебхука, если используется
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# Настройки логирования
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = 'bot.log'

# Настройки базы данных (если потребуется в будущем)
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///bot_db.sqlite')

# Другие константы
HELP_MESSAGE = """
Доступные команды:
/start - Начать работу с ботом
/help - Показать это сообщение
"""

START_MESSAGE = "Привет! Я твой новый телеграм бот. Используй /help для просмотра доступных команд."
