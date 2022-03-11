import telebot
from conf import db_name, bot_token
import psycopg2


bot = telebot.TeleBot(bot_token)
conn_db = psycopg2.connect(db_name)
cur = conn_db.cursor()
