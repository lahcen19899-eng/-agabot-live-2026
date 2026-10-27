import os
import telebot
import requests
from flask import Flask, request

BOT_TOKEN = '8822777566:AAHuRTTtHUL0239Wcg1A2IuxEPEhnxix1pU'
API_FOOTBALL_KEY = 'f3b98d7a965f4c248b911d8b9a3e6d52'

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# إعادة ضبط الويب هوك قسرياً عند إقلاع السيرفر
WEBHOOK_URL = f'https://agabot-live-2026-1.onrender.com/{BOT_TOKEN}'
try:
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
except Exception as e:
    print(f"Webhook setup error: {e}")

@app.route('/' + BOT_TOKEN, methods=['POST'])
def get_message():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return '!', 200
    else:
        return 'Not Found', 404

@app.route("/")
def index():
    return 'Bot is running successfully!', 200

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "مرحباً بك في بوت النتائج المباشرة لكرة القدم! أرسل /live لمعرفة النتائج الحالية.")

@bot.message_handler(commands=['live', 'matches'])
def send_live_scores(message):
    bot.reply_to(message, "جاري جلب النتائج... يرجى الانتظار.")
    url = "https://api.football-data.org/v4/matches?status=LIVE"
    headers = {'X-Auth-Token': API_FOOTBALL_KEY}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            matches = data.get('matches', [])
            if matches:
                text = " المباريات الجارية الآن:\n"
                for match in matches[:5]:
                    home = match['homeTeam']['name']
                    away = match['awayTeam']['name']
                    text += f"- {home} vs {away}\n"
                bot.reply_to(message, text)
            else:
                bot.reply_to(message, "⏳ لا توجد مباريات جارية في هذه اللحظة بالضبط. جرب لاحقاً عندما تبدأ المباريات الحية!")
        else:
            bot.reply_to(message, "عذراً، حدث خطأ في الاتصال بمزود البيانات.")
    except Exception as e:
        bot.reply_to(message, "عذراً، حدث خطأ أثناء جلب النتائج.")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
