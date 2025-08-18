import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from core.infrastructure.database.database_manager import DatabaseManager
from core.infrastructure.database.repositories.stock_repository import StockRepository

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я бот для учета остатков.\n"
        "Напиши /stock чтобы проверить, чего мало на складе"
    )


async def stock_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        db = DatabaseManager()
        stock_repo = StockRepository(db.get_connection())

        low_stock = stock_repo.get_low_stock_items()

        if not low_stock:
            await update.message.reply_text("✅ Все ингредиенты в норме!")
        else:
            message = "Осталось мало:\n"
            for name, quantity in low_stock:
                message += f"• {name}: {quantity}\n"
            await update.message.reply_text(message)

    except Exception as e:
        await update.message.reply_text("😢 Ошибка при проверке склада")


def run_bot():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stock", stock_command))

    print("Бот запущен...")
    app.run_polling()


if __name__ == "__main__":
    run_bot()