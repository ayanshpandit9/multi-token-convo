import telebot
from telebot import types
from instagram_private_api import Client, ClientCookieAuthError
import time
import os

bot = telebot.TeleBot("8003051865:AAFU_jM4OAvfeYHw0eDMQ9FLAAKcvJS9200")

user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Welcome! Send /send to start sending Instagram DMs.")

@bot.message_handler(commands=['send'])
def send(message):
    user_data[message.chat.id] = {}
    msg = bot.send_message(message.chat.id, "Send your Instagram cookie string:")
    bot.register_next_step_handler(msg, get_cookie)

def get_cookie(message):
    cookie = message.text.strip()
    user_data[message.chat.id]['cookie'] = cookie
    msg = bot.send_message(message.chat.id, "Enter the Instagram thread ID:")
    bot.register_next_step_handler(msg, get_thread_id)

def get_thread_id(message):
    thread_id = message.text.strip()
    user_data[message.chat.id]['thread_id'] = thread_id
    msg = bot.send_message(message.chat.id, "Enter the name to prefix in each message:")
    bot.register_next_step_handler(msg, get_name)

def get_name(message):
    name = message.text.strip()
    user_data[message.chat.id]['name'] = name
    msg = bot.send_message(message.chat.id, "Now upload the message text file (.txt):")
    bot.register_next_step_handler(msg, get_file)

def get_file(message):
    if not message.document:
        bot.send_message(message.chat.id, "Please send a .txt file.")
        return

    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    filepath = f"{message.chat.id}_messages.txt"
    with open(filepath, "wb") as f:
        f.write(downloaded_file)

    user_data[message.chat.id]['msgfile'] = filepath
    msg = bot.send_message(message.chat.id, "Enter delay (in seconds) between messages:")
    bot.register_next_step_handler(msg, get_delay)

def get_delay(message):
    try:
        delay = int(message.text.strip())
    except:
        bot.send_message(message.chat.id, "Enter a valid number for delay.")
        return

    user_data[message.chat.id]['delay'] = delay
    bot.send_message(message.chat.id, "Starting DM sending...")
    send_messages(message.chat.id)

def send_messages(chat_id):
    data = user_data.get(chat_id)
    if not data:
        return

    cookie_string = data['cookie']
    thread_id = data['thread_id']
    name = data['name']
    filepath = data['msgfile']
    delay = data['delay']

    try:
        cookie_dict = {}
        for part in cookie_string.split(';'):
            if '=' in part:
                key, value = part.strip().split('=', 1)
                cookie_dict[key.strip()] = value.strip()

        api = Client(cookie=None, auto_patch=True, authenticate=False)
        api._initiate_session()
        api._session.cookies.update(cookie_dict)
        api.authenticated_user_id = api.current_user()['user']['pk']

        with open(filepath, "r", encoding="utf-8") as f:
            messages = [line.strip() for line in f if line.strip()]

        for msg in messages:
            full_msg = f"{name} {msg}"
            api.direct_v2_send_text(recipient_users=[[thread_id]], text=full_msg)
            bot.send_message(chat_id, f"✅ Sent: {full_msg}")
            time.sleep(delay)

        bot.send_message(chat_id, "✅ Done sending all messages.")
        os.remove(filepath)

    except ClientCookieAuthError:
        bot.send_message(chat_id, "❌ Invalid cookie or session expired.")
    except Exception as e:
        bot.send_message(chat_id, f"⚠️ Error: {e}")

bot.polling()
