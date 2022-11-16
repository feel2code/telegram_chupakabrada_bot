import os
import psycopg2
import telebot

from dotenv import load_dotenv

load_dotenv(f"{'/'.join(os.getcwd().split('/')[:5])}/.env")


bot = telebot.TeleBot(os.getenv('BOT_TOKEN'))
conn_db = psycopg2.connect(os.getenv('DB'))
cur = conn_db.cursor()
