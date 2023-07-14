import os
import telebot
import mysql.connector

from dotenv import load_dotenv

load_dotenv(f"{'/'.join(os.getcwd().split('/')[:5])}/.env")


bot = telebot.TeleBot(os.getenv('BOT_TOKEN'))
conn_db = mysql.connector.connect(user=os.getenv('DB_USER'),
                                  password=os.getenv('DB_PASSWORD'),
                                  host='127.0.0.1',
                                  database=os.getenv('DB_NAME'))
cur = conn_db.cursor()
