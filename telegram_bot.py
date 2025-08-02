import time
import pytz
import telebot
import schedule
import threading
from datetime import datetime
from coffee_shop import low_stock

MOSCOW_TZ = pytz.timezone('Europe/Moscow')
NOTIFICATION_TIME = "19:00"
TOKEN = "8370067382:AAHJdPF_E3wBgIY2B-SgY4GHwfx64gMgabM"
bot = telebot.TeleBot(TOKEN)
subscribers = set()
subscribers_lock = threading.Lock()

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    with subscribers_lock:
        if chat_id not in subscribers:
            subscribers.add(chat_id)
            bot.reply_to(message, "Вы подписались на уведомления!")
        else:
            bot.reply_to(message, "Вы уже подписаны")

@bot.message_handler(commands=['stop'])
def stop(message):
    chat_id = message.chat.id
    with subscribers_lock:
        if chat_id in subscribers:
            subscribers.remove(chat_id)
            bot.reply_to(message, "Вы отписались от уведомлений")
        else:
            bot.reply_to(message, "Вы не были подписаны")

@bot.message_handler(commands=['inventory'])
def handle_inventory(message):
    bot.reply_to(message, low_stock())


def send_scheduled_notification():
    try:
        inventory_list = low_stock()
        message = "Ежедневный отчет по инвентарю:\n\n" + inventory_list
        with subscribers_lock:
            current_subscribers = list(subscribers)

        for chat_id in current_subscribers:
            try:
                bot.send_message(chat_id, message)
                print(f"[{datetime.now(MOSCOW_TZ)}] Уведомление отправлено {chat_id}")
            except Exception as e:
                print(f"Ошибка отправки {chat_id}: {str(e)}")
                if "bot was blocked" in str(e).lower() or "Forbidden" in str(e):
                    with subscribers_lock:
                        subscribers.discard(chat_id)
    except Exception as e:
        print(f"Ошибка формирования уведомления: {str(e)}")

def schedule_checker():
    while True:
        schedule.run_pending()
        time.sleep(60)


print("Бот запущен!")
schedule.every().day.at(NOTIFICATION_TIME, MOSCOW_TZ).do(send_scheduled_notification)
scheduler_thread = threading.Thread(target=schedule_checker, daemon=True)
scheduler_thread.start()
bot.infinity_polling()