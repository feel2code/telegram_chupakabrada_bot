import time
import telebot
from conf import name, conn
import random
from sys import argv
import psycopg2

script, chat = argv
bot = telebot.TeleBot(name)
conn_db = psycopg2.connect(conn)
cur = conn_db.cursor()

time.sleep(random.randint(1, 15800))
cur.execute(
    "SELECT ask_answer FROM asking where ask_id="
    + str(random.randint(1, 9)) + " ")
records = cur.fetchall()
rec = (str(records[0]).replace("('", "")).replace("',)", "").replace(")", "")
bot.send_message(chat_id=chat, text=rec)
