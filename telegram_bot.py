import telebot
import threading
import time
import logging
from queue import Queue, Empty

bot = telebot.TeleBot('8370067382:AAHJdPF_E3wBgIY2B-SgY4GHwfx64gMgabM')

subscribers_lock = threading.RLock()
subscribers = set()
notification_queue = Queue()
active = threading.Event()
active.set()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('cafe_bot.log')
    ]
)
logger = logging.getLogger('CafeBot')


@bot.message_handler(commands=['start'])
def handle_start(message):
    chat_id = message.chat.id
    with subscribers_lock:
        if chat_id not in subscribers:
            subscribers.add(chat_id)
            response = "✅ Вы подписались на уведомления о продуктах!"
            logger.info(f"New subscriber: {chat_id}")
        else:
            response = "ℹ️ Вы уже подписаны!"

    bot.reply_to(message, response)


@bot.message_handler(commands=['stop'])
def handle_stop(message):
    chat_id = message.chat.id
    with subscribers_lock:
        if chat_id in subscribers:
            subscribers.remove(chat_id)
            response = "❌ Вы отписались от уведомлений"
            logger.info(f"Unsubscribed: {chat_id}")
        else:
            response = "ℹ️ Вы не были подписаны"

    bot.reply_to(message, response)


@bot.message_handler(commands=['status'])
def handle_status(message):
    chat_id = message.chat.id
    with subscribers_lock:
        status = "подписаны" if chat_id in subscribers else "не подписаны"

    bot.reply_to(message, f"🔔 Статус: Вы {status} на уведомления")


@bot.message_handler(commands=['inventory'])
def handle_inventory(message):
    low_stock = {"Кофе": 5, "Молоко": 3, "Сахар": 2}

    response = "⚠️ Низкие запасы:\n"
    response += "\n".join([f"- {product}: {qty} кг" for product, qty in low_stock.items()])

    bot.reply_to(message, response)


def notify_low_stock(product_name):
    """Постановка уведомления в очередь (вызывается из основной программы)"""
    if not active.is_set():
        logger.warning("Bot is shutting down. Notification discarded.")
        return

    notification_queue.put(product_name)
    logger.info(f"Notification queued: {product_name}")


def notification_worker():
    """Рабочий поток для обработки уведомлений"""
    logger.info("Notification worker started")
    while active.is_set() or not notification_queue.empty():
        try:
            product_name = notification_queue.get(timeout=1.0)

            with subscribers_lock:
                current_subscribers = list(subscribers)

            for chat_id in current_subscribers:
                try:
                    bot.send_message(
                        chat_id,
                        f"🚨 СРОЧНО! Продукт '{product_name}' на критическом уровне!"
                    )
                    logger.debug(f"Sent to {chat_id}")
                except telebot.apihelper.ApiTelegramException as e:
                    if e.error_code == 403:
                        with subscribers_lock:
                            if chat_id in subscribers:
                                subscribers.remove(chat_id)
                                logger.warning(f"Removed blocked user: {chat_id}")
                    else:
                        logger.error(f"API error: {e}")
                except Exception as e:
                    logger.exception(f"Unexpected error: {e}")

            notification_queue.task_done()
            logger.debug(f"Processed: {product_name}")

        except Empty:
            continue
        except Exception as e:
            logger.exception(f"Worker error: {e}")
            time.sleep(1)


def run_bot():
    logger.info("Starting bot polling")
    while active.is_set():
        try:
            bot.polling(none_stop=True, timeout=20)
        except Exception as e:
            logger.error(f"Polling error: {e}")
            time.sleep(5)


def shutdown():
    logger.info("Initiating shutdown sequence")
    active.clear()

    notification_queue.join()
    logger.info("All notifications processed. System shutdown")


if __name__ == "__main__":
    try:
        worker_thread = threading.Thread(
            target=notification_worker,
            name="NotificationWorker",
            daemon=True
        )
        worker_thread.start()

        run_bot()

    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received")
        shutdown()
    except Exception as e:
        logger.exception("Fatal error in main")
        shutdown()
    finally:
        logger.info("Application terminated")