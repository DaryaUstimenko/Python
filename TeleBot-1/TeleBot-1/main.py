import random
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = "8324467854:AAEdzkM_2e6z3WVyO0zb6UTZxR4Ws1np-ZY"

FIXED_RESPONSES = {
    "писатель": "Хемингуэй",
    "поэт": "Шекспир",
    "книга": "Три товарища",
    "монолог": "Быть или не быть"
}

RANDOM_WRITERS = ["Хемингуэй", "Достоевский", "Толстой", "Чехов", "Гоголь", "Пушкин", "Набоков"]
RANDOM_POETS = ["Шекспир", "Пушкин", "Лермонтов", "Блок", "Есенин", "Маяковский", "Ахматова"]
RANDOM_BOOKS = ["Три товарища", "Война и мир", "Преступление и наказание", "Мастер и Маргарита",
                "Анна Каренина", "Евгений Онегин", "Тихий Дон"]
RANDOM_MONOLOGUES = ["Быть или не быть", "Монолог Чацкого", "Монолог Германна",
                     "Монолог Раскольникова", "Монолог Анны Карениной"]


def get_random_response(category):
    category_lower = category.lower()

    if category_lower == "писатель":
        return random.choice(RANDOM_WRITERS)
    elif category_lower == "поэт":
        return random.choice(RANDOM_POETS)
    elif category_lower == "книга":
        return random.choice(RANDOM_BOOKS)
    elif category_lower == "монолог":
        return random.choice(RANDOM_MONOLOGUES)
    else:
        return None


def get_fixed_response(category):
    category_lower = category.lower()
    return FIXED_RESPONSES.get(category_lower)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я бот-эрудит. Я знаю писателей, поэтов, книги и монологи!\n\n"
        "Отправь мне одно из слов:\n"
        "• Писатель\n"
        "• Поэт\n"
        "• Книга\n"
        "• Монолог\n\n"
        "Я отвечу тебе классическим (фиксированным) вариантом!\n\n"
        "А если хочешь случайный ответ — напиши команду /random\n"
        "А затем отправь слово (Писатель/Поэт/Книга/Монолог)\n\n"
        "Или используй команды:\n"
        "/fixed - фиксированный режим (по умолчанию)\n"
        "/random - случайный режим\n"
        "/info - информация о боте"
    )


async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Бот создан для ответов на литературные вопросы.\n\n"
        "Режимы работы:\n"
        "• Фиксированный режим — всегда один и тот же ответ\n"
        "• Случайный режим — каждый раз новый ответ из списка\n\n"
        "Для переключения режима используй:\n"
        "/fixed - фиксированный режим\n"
        "/random - случайный режим"
    )


async def set_fixed_mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['mode'] = 'fixed'
    await update.message.reply_text("✅ Режим изменен на ФИКСИРОВАННЫЙ (всегда один ответ)")


async def set_random_mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['mode'] = 'random'
    await update.message.reply_text("🎲 Режим изменен на СЛУЧАЙНЫЙ (разные ответы)")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.strip()

    mode = context.user_data.get('mode', 'fixed')

    if user_text.lower() in ["писатель", "поэт", "книга", "монолог"]:

        if mode == 'random':
            answer = get_random_response(user_text)
            await update.message.reply_text(f"🎲 {answer}")
        else:
            answer = get_fixed_response(user_text)
            await update.message.reply_text(f"📖 {answer}")
    else:
        await update.message.reply_text(
            "❌ Я понимаю только команды:\n"
            "• Писатель\n"
            "• Поэт\n"
            "• Книга\n"
            "• Монолог\n\n"
            "Используй /start для справки"
        )


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Ошибка: {context.error}")
    if update and update.message:
        await update.message.reply_text("Произошла ошибка. Попробуйте позже.")


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # Регистрируем обработчики команд
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("info", info))
    app.add_handler(CommandHandler("fixed", set_fixed_mode))
    app.add_handler(CommandHandler("random", set_random_mode))

    # Регистрируем обработчик текстовых сообщений
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Регистрируем обработчик ошибок
    app.add_error_handler(error_handler)

    # Запускаем бота (убираем параметр allowed_updates)
    print("Бот запущен...")
    app.run_polling()


if __name__ == "__main__":
    main()