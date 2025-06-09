import telebot
import time
import random
import os
from datetime import datetime, timedelta
import pytz

# === CONFIG ===
TOKEN = '7838288204:AAHnAOvkuaQyGb_5XaJMOPpWOxhUL_1_PEg'   # Replace with your bot token
CHAT_ID = '7843995956'       # Replace with your chat ID
TEXT_FILE = 'texts/meet_dec_count.txt'
POSITION_FILE = 'texts/position.txt'
JAPAN_TZ = pytz.timezone("Asia/Tokyo")

WAKE_START_HOUR = 9   # 9 AM Japan time
WAKE_END_HOUR = 22    # 10 PM Japan time

bot = telebot.TeleBot(TOKEN)

def load_messages():
    with open(TEXT_FILE, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]
    return lines

def load_position():
    if os.path.exists(POSITION_FILE):
        with open(POSITION_FILE, 'r') as f:
            return int(f.read().strip())
    return 0

def save_position(pos):
    with open(POSITION_FILE, 'w') as f:
        f.write(str(pos))

def is_waking_hours():
    now = datetime.now(JAPAN_TZ)
    return WAKE_START_HOUR <= now.hour < WAKE_END_HOUR

def wait_until_waking_hours():
    while not is_waking_hours():
        print("Sleeping hours in Japan... waiting 30 minutes.")
        time.sleep(1800)

def send_next_message():
    messages = load_messages()
    pos = load_position()
    
    if pos >= len(messages):
        print("All messages sent.")
        return False

    message = messages[pos]
    bot.send_message(CHAT_ID, message)
    print(f"Sent message: {message}")
    save_position(pos + 1)
    return True

def send_daily_messages():
    while True:
        sent_count = 0
        while sent_count < 3:
            wait_until_waking_hours()

            if not send_next_message():
                return
            
            sent_count += 1

            if sent_count < 3:
                # delay = random.randint(4 * 3600, 6 * 3600)
                # print(f"Waiting {delay // 3600} hours and {(delay % 3600) // 60} minutes for next message...")
                # time.sleep(delay)

                delay = random.randint(10, 15)  # seconds
                print(f"[TEST MODE] Waiting {delay} seconds for next message...")
                time.sleep(3)




        # Wait until 00:05 Japan time next day
        now = datetime.now(JAPAN_TZ)
        tomorrow = (now + timedelta(days=1)).replace(hour=0, minute=5, second=0, microsecond=0)
        wait_seconds = (tomorrow - now).total_seconds()
        print(f"Sleeping until next day: {wait_seconds // 3600:.1f} hours")
        #time.sleep(wait_seconds)
        time.sleep(5)



bot.send_message(CHAT_ID, "worked")

# === Start the bot loop ===
send_daily_messages()
