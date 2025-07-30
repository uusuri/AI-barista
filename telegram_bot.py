import telebot
import threading
from queue import Queue

TOKEN = ""
bot = telebot.TeleBot(TOKEN)

subscribers = set()
subscribers_lock = threading.Lock()
notification_queue = Queue()

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    with subscribers_lock:
        if chat_id not in subscribers:
            subscribers.add(chat_id)
            bot.reply_to(message, "✅ Вы подписались на уведомления!")
        else:
            bot.reply_to(message, "ℹ️ Вы уже подписаны")

@bot.message_handler(commands=['stop'])
def stop(message):
    chat_id = message.chat.id
    with subscribers_lock:
        if chat_id in subscribers:
            subscribers.remove(chat_id)
            bot.reply_to(message, "❌ Вы отписались от уведомлений")
        else:
            bot.reply_to(message, "ℹ️ Вы не были подписаны")

@bot.message_handler(commands=['inventory'])
def inventory(message):
    bot.reply_to(message, "☕ Сейчас в наличии: латте, капучино, раф")

print("Бот запущен!")
bot.infinity_polling()