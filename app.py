import os
from flask import Flask, request
import telebot
import requests
import random

TOKEN = '8967248749:AAEeLGEnpZWGhr_RZgwoWbJo_sSZm2DI9z8'
bot = telebot.TeleBot(TOKEN)

API_KEY = '944ddf58919e4bd4bf942b812bd2f4c6'
BASE_URL = 'https://api.football-data.org/v4/matches?status=IN_PLAY,PAUSED'

app = Flask(__name__)

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return '!', 200

@app.route('/')
def index():
    return 'Bot is running 24/7 successfully!', 200

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "مرحباً بك! بوت تحليل المباريات المباشرة يعمل الآن على السحابة 24/7 ⚽\nأرسل /live لعرض المباريات الجارية.")

@bot.message_handler(commands=['live', 'matches'])
def get_live_matches(message):
    bot.reply_to(message, "🔍 جاري البحث عن المباريات المباشرة والجارية الآن...")
    
    headers = {'X-Auth-Token': API_KEY}
    
    try:
        response = requests.get(BASE_URL, headers=headers)
        
        if response.status
