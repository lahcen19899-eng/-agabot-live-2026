import os
import telebot
import requests
from flask import Flask, request

# --- إعدادات البوت الأساسية ---
BOT_TOKEN = '8967248759:AAEeLGENpZWGhr_RZgwOWbJo_sSZm2DI9z8'
API_FOOTBALL_KEY = 'f3b98d7a965f4c248b911d8b9a3e6d52'

# --- تهيئة البوت ---
bot = telebot.TeleBot(BOT_TOKEN)
server = Flask(__name__)

# --- وظائف البوت ---
def get_live_scores():
    """
    وظيفة لجلب النتائج المباشرة.
    """
    url = "https://api.football-data.org/v4/matches?status=LIVE"
    headers = {
        'X-Auth-Token': API_FOOTBALL_KEY
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
             data = response.json()
             return data
        else:
             print(f"API Error: Status Code {response.status_code}")
             return None
    except Exception as e:
        print(f"Exception in get_live_scores: {e}")
        return None

# --- معالجة أوامر تيليجرام ---
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "مرحباً بك في بوت النتائج المباشرة لكرة القدم! أرسل /live لمعرفة النتائج الحالية.")

@bot.message_handler(commands=['live'])
def send_live_scores(message):
    bot.reply_to(message, "جاري جلب النتائج المباشرة... يرجى الانتظار.")
    scores = get_live_scores()
    if scores:
        bot.reply_to(message, "تم جلب البيانات بنجاح!")
    else:
        bot.reply_to(message, "عذراً، حدث خطأ أثناء جلب النتائج. يرجى المحاولة لاحقاً.")

# --- إعدادات Webhook لـ Render ---
@server.route('/' + BOT_TOKEN, methods=['POST'])
def get_message():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return '!', 200
    else:
        return 'Not Found', 404

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://agabot-live-2026-1.onrender.com' + '/' + BOT_TOKEN)
    return 'Bot is running!', 200

# --- التشغيل الرئيسي ---
if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
