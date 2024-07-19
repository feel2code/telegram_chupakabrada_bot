import os
import sqlite3
from sqlite3 import DatabaseError, OperationalError

import telebot
from dotenv import load_dotenv

load_dotenv(".env")
bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))


class SQLUtils:
    conn = None

    def connect(self):
        self.conn = sqlite3.connect(f'{os.getenv("DB_NAME")}.db')

    def query(self, request):
        try:
            cursor = self.conn.cursor()
            cursor.execute(request)
        except (AttributeError, DatabaseError, OperationalError):
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute(request)
        return cursor.fetchall()

    def mutate(self, request):
        try:
            cursor = self.conn.cursor()
            cursor.execute(request)
            self.conn.commit()
        except (AttributeError, DatabaseError, OperationalError):
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute(request)
            self.conn.commit()
        return cursor
