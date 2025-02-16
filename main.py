from database import load_database, excel_to_json, search_product
from telebot.types import Message
from config import *
import telebot
import time

bot = telebot.TeleBot(BOT_TOKEN)

database = load_database()

# @bot.message_handler(func=lambda message: True, content_types=['text'])
# def handle_message(message):
#     # database = load_database()
#     response = search_product(message.text, database)
#     bot.reply_to(message, response)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    query = message.text.split(" ", 1)[1] if len(message.text.split(" ", 1)) > 1 else None

    try:
        bot.send_message(message.chat.id,  "👋 سلام! به فروشگاه صفر زاده خوش آمدید.")
    except Exception as e:
        print(f"error while{e}")
    if query:
        # database = load_database()
        response = search_product(query, database)
        bot.send_message(message.chat.id, response)


# @bot.message_handler(func=lambda message: True, content_types=['text'])
# def handle_message(message):
#     # database = load_database()
#     response = search_product(message.text, database)
#
#     if message.chat.type == "group" or message.chat.type == "supergroup":
#         try:
#             bot.send_message(message.from_user.id, response)
#         except:
#             start_link = f"https://t.me/SafarZadehRobot?start={message.text}"
#             bot.reply_to(message,
#                          f"⚠️ لطفاً [اینجا را کلیک کنید]({start_link}) و ربات را استارت کنید تا اطلاعات برای شما ارسال شود.",
#                          parse_mode="Markdown")
#     else:
#         bot.reply_to(message, response)

@bot.message_handler(content_types=['document'])
def upload_excel(message: Message):
    if message.chat.id != ADMIN_ID:
        bot.reply_to(message, "❌ شما دسترسی ادمین ندارید.")
        return

    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    file_path = "products.xlsx"

    with open(file_path, "wb") as file:
        file.write(downloaded_file)

    if excel_to_json(file_path):
        global database
        database = load_database()
        bot.reply_to(message, "✅ فایل اکسل با موفقیت آپلود و به JSON تبدیل شد.")
    else:
        bot.reply_to(message, "❌ خطا در پردازش فایل اکسل.")


import json

STATUS_FILE = "status.json"

def get_bot_status():
    """دریافت وضعیت فعال یا غیرفعال بودن ربات"""
    try:
        with open(STATUS_FILE, "r") as file:
            status = json.load(file)
            return status.get("active", True)
    except:
        return True

def toggle_bot_status():
    current_status = get_bot_status()
    new_status = not current_status
    with open(STATUS_FILE, "w") as file:
        json.dump({"active": new_status}, file)
    return new_status

@bot.message_handler(commands=['toggle'])
def toggle_bot(message):
    if message.from_user.id == ADMIN_ID:  # فقط ادمین اجازه تغییر دارد
        new_status = toggle_bot_status()
        status_text = "✅ ربات در گروه‌ها فعال شد!" if new_status else "❌ ربات در گروه‌ها غیرفعال شد!"
        bot.reply_to(message, status_text)
    else:
        bot.reply_to(message, "⛔ شما اجازه این کار را ندارید.")


@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_message(message):
    if message.chat.type in ["group", "supergroup"] and not get_bot_status():
        return

    response = search_product(message.text, database)

    if message.chat.type == "group" or message.chat.type == "supergroup":
        try:
            bot.send_message(message.from_user.id, response)  # ارسال پیام در پی‌وی
        except:
            start_link = f"https://t.me/YOUR_BOT_USERNAME?start={message.text}"
            bot.reply_to(message,
                         f"⚠️ لطفاً [اینجا را کلیک کنید]({start_link}) و ربات را استارت کنید تا اطلاعات برای شما ارسال شود.",
                         parse_mode="Markdown")
    else:
        bot.reply_to(message, response)


while True:
    try:
        bot.polling(none_stop=True, interval=1, timeout=20)
    except Exception as e:
        print(f"Polling Error: {e}")
        time.sleep(5)