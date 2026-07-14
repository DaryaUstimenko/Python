import logging
from telegram import Update, BotCommand, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram_bot.config import BOT_TOKEN, LOG_FILE, LOG_LEVEL, START_MESSAGE, HELP_MESSAGE
from telegram_bot.events_data import (get_events_by_date, get_theater_events,
                         get_concert_events, get_all_future_events, format_event)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=getattr(logging, LOG_LEVEL),
    filename=LOG_FILE
)
logger = logging.getLogger(__name__)

# Определяем команды бота
BOT_COMMANDS = [
    BotCommand("start", "Запустить бота"),
    BotCommand("help", "Показать справку"),
    BotCommand("menu", "Показать главное меню"),
    BotCommand("about", "О боте"),
    BotCommand("settings", "Настройки"),
    BotCommand("date", "Показать события на дату (формат: /date ДД.ММ.ГГГГ)"),
    BotCommand("theater", "Показать театральные события"),
    BotCommand("concert", "Показать концерты"),
    BotCommand("all", "Показать все будущие события")
]

# Клавиатура главного меню
MAIN_KEYBOARD = ReplyKeyboardMarkup([
    [KeyboardButton("📝 Помощь"), KeyboardButton("ℹ️ О боте")],
    [KeyboardButton("⚙️ Настройки"), KeyboardButton("📊 Статистика")]
], resize_keyboard=True)


# Обработчики команд
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    try:
        user = update.effective_user
        logger.info(f"Пользователь {user.id} запустил бота")
        await update.message.reply_text(START_MESSAGE)
    except Exception as e:
        logger.error(f"Ошибка в команде start: {e}")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /help"""
    try:
        logger.info(f"Пользователь {update.effective_user.id} запросил помощь")
        await update.message.reply_text(HELP_MESSAGE)
    except Exception as e:
        logger.error(f"Ошибка в команде help: {e}")


# Новые обработчики сообщений
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик текстовых сообщений"""
    try:
        user = update.effective_user
        text = update.message.text
        logger.info(f"Получено сообщение от {user.id}: {text}")

        # Обработка кнопок меню
        if text == "📝 Помощь":
            await help_command(update, context)
        elif text == "ℹ️ О боте":
            await about_command(update, context)
        elif text == "⚙️ Настройки":
            await settings_command(update, context)
        elif text == "📊 Статистика":
            await update.message.reply_text("Статистика временно недоступна")
        else:
            # Эхо-ответ для остальных сообщений
            response = f"Вы написали: {text}"
            await update.message.reply_text(response)
    except Exception as e:
        logger.error(f"Ошибка при обработке текстового сообщения: {e}")


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик фотографий"""
    try:
        user = update.effective_user
        logger.info(f"Получено фото от {user.id}")
        await update.message.reply_text("Я получил ваше фото!")
    except Exception as e:
        logger.error(f"Ошибка при обработке фото: {e}")


async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик документов"""
    try:
        user = update.effective_user
        logger.info(f"Получен документ от {user.id}")
        await update.message.reply_text("Я получил ваш документ!")
    except Exception as e:
        logger.error(f"Ошибка при обработке документа: {e}")


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик ошибок"""
    logger.error(f"Update {update} caused error {context.error}")


# Добавляем новые обработчики команд
async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показать главное меню"""
    try:
        user = update.effective_user
        logger.info(f"Пользователь {user.id} открыл меню")
        await update.message.reply_text(
            "Выберите действие:",
            reply_markup=MAIN_KEYBOARD
        )
    except Exception as e:
        logger.error(f"Ошибка в команде menu: {e}")


async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Информация о боте"""
    try:
        await update.message.reply_text(
            "🤖 Это базовый телеграм бот.\n"
            "Версия: 1.0\n"
            "Автор: Ваше имя"
        )
    except Exception as e:
        logger.error(f"Ошибка в команде about: {e}")


async def settings_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Настройки бота"""
    try:
        await update.message.reply_text(
            "⚙️ Настройки бота:\n"
            "В разработке..."
        )
    except Exception as e:
        logger.error(f"Ошибка в команде settings: {e}")


async def setup_commands(application: Application):
    """Установка команд бота"""
    await application.bot.set_my_commands(BOT_COMMANDS)


async def date_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /date"""
    try:
        # Получаем дату из аргументов команды
        if not context.args:
            await update.message.reply_text(
                "Пожалуйста, укажите дату в формате ДД.ММ.ГГГГ\n"
                "Например: /date 30.03.2024"
            )
            return

        date_str = context.args[0]
        events = get_events_by_date(date_str)

        if events is None:
            await update.message.reply_text(
                "Неверный формат даты. Используйте формат ДД.ММ.ГГГГ"
            )
            return

        if not events:
            await update.message.reply_text(f"На {date_str} событий не найдено")
            return

        response = f"События на {date_str}:\n\n"
        response += "\n".join(format_event(event) for event in events)
        await update.message.reply_text(response)

    except Exception as e:
        logger.error(f"Ошибка в команде date: {e}")
        await update.message.reply_text("Произошла ошибка при обработке команды")


async def theater_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /theater"""
    try:
        events = get_theater_events()
        if not events:
            await update.message.reply_text("Театральных событий не найдено")
            return

        response = "Предстоящие театральные события:\n\n"
        response += "\n".join(format_event(event) for event in events)
        await update.message.reply_text(response)

    except Exception as e:
        logger.error(f"Ошибка в команде theater: {e}")
        await update.message.reply_text("Произошла ошибка при обработке команды")


async def concert_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /concert"""
    try:
        events = get_concert_events()
        if not events:
            await update.message.reply_text("Концертов не найдено")
            return

        response = "Предстоящие концерты:\n\n"
        response += "\n".join(format_event(event) for event in events)
        await update.message.reply_text(response)

    except Exception as e:
        logger.error(f"Ошибка в команде concert: {e}")
        await update.message.reply_text("Произошла ошибка при обработке команды")


async def all_events_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /all"""
    try:
        events = get_all_future_events()
        if not events:
            await update.message.reply_text("Будущих событий не найдено")
            return

        response = "Все предстоящие события:\n\n"
        response += "\n".join(format_event(event) for event in events)
        await update.message.reply_text(response)

    except Exception as e:
        logger.error(f"Ошибка в команде all: {e}")
        await update.message.reply_text("Произошла ошибка при обработке команды")


def main():
    """Основная функция"""
    try:
        # Создаем приложение бота
        application = Application.builder().token(BOT_TOKEN).build()

        # Устанавливаем команды бота
        application.job_queue.run_once(
            lambda context: setup_commands(application),
            when=0
        )

        # Добавляем обработчики команд
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("menu", menu_command))
        application.add_handler(CommandHandler("about", about_command))
        application.add_handler(CommandHandler("settings", settings_command))
        application.add_handler(CommandHandler("date", date_command))
        application.add_handler(CommandHandler("theater", theater_command))
        application.add_handler(CommandHandler("concert", concert_command))
        application.add_handler(CommandHandler("all", all_events_command))

        # Добавляем обработчики сообщений
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
        application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
        application.add_handler(MessageHandler(filters.Document.ALL, handle_document))

        # Добавляем обработчик ошибок
        application.add_error_handler(error_handler)

        # Запускаем бота
        logger.info("Бот запущен")
        application.run_polling(allowed_updates=Update.ALL_TYPES)

    except Exception as e:
        logger.critical(f"Критическая ошибка: {e}")


if __name__ == '__main__':
    main()
