import psycopg2
import telebot

from conf import bot_token, db_name

bot = telebot.TeleBot(bot_token)
conn_db = psycopg2.connect(db_name)
cur = conn_db.cursor()
