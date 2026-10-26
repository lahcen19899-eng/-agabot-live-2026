import os
import telebot
import requests
from flask import Flask, request

# --- إعدادات البوت الأساسية ---
BOT_TOKEN = '8967248759:AAEeLGENpZWGhr_RZgwOWbJo_sSZm2DI9z8'
API_FOOTBALL_KEY = 'f3b98d7a965f4c248b911d8b9a3e6d52'

# --- تهيئة البوت ---
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

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
@
