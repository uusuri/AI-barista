import pytz
from telebot import TeleBot
import threading

from core.infrastructure.database.database_manager import DatabaseManager
from core.infrastructure.services import MenuService
from infrastructure import StockRepository

db = DatabaseManager()
moscow_tz = pytz.timezone('Europe/Moscow')
notification_time = "19:00"
bot = TeleBot("8370067382:AAHJdPF_E3wBgIY2B-SgY4GHwfx64gMgabM")
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
    try:
        with db.get_connection() as conn:
            stock_repo = StockRepository(conn)
            menu_service = MenuService(menu_repo = None, stock_repo=stock_repo)

            response = menu_service.get_low_stock_alert()
            bot.reply_to(message, response)

    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {str(e)}")

# def send_scheduled_notification():
#     try:
#         inventory_list = fetch_low_stock(get_connection(databasePath))
#         message = "Ежедневный отчет по инвентарю:\n\n" + inventory_list
#         with subscribers_lock:
#             current_subscribers = list(subscribers)
#
#         for chat_id in current_subscribers:
#             try:
#                 bot.send_message(chat_id, message)
#                 print(f"[{datetime.datetime.now(MOSCOW_TZ)}] Уведомление отправлено {chat_id}")
#             except Exception as e:
#                 print(f"Ошибка отправки {chat_id}: {str(e)}")
#                 if "bot was blocked" in str(e).lower() or "Forbidden" in str(e):
#                     with subscribers_lock:
#                         subscribers.discard(chat_id)
#     except Exception as e:
#         print(f"Ошибка формирования уведомления: {str(e)}")
#
# def schedule_checker():
#     while True:
#         schedule.run_pending()
#         time.sleep(60)
#
#
# print("Бот запущен!")
# schedule.every().day.at(NOTIFICATION_TIME, MOSCOW_TZ).do(send_scheduled_notification)
# scheduler_thread = threading.Thread(target=schedule_checker, daemon=True)
# scheduler_thread.start()
bot.infinity_polling()