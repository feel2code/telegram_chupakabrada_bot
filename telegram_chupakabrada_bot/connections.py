import os
import sqlite3
from sqlite3 import DatabaseError, OperationalError

import telebot
from dotenv import load_dotenv

load_dotenv(".env")
bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))
env_path = os.getenv("ENV_PATH", "")


class SQLUtils:
    conn = None

    def connect(self):
        self.conn = sqlite3.connect(f'{env_path}{os.getenv("DB_NAME")}.db')

    def query(self, request):
        try:
            cursor = self.conn.cursor()
            cursor.execute(request)
        except (AttributeError, DatabaseError, OperationalError):
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute(request)
        fetched = cursor.fetchall()
        if len(fetched) == 1:
            if len(fetched[0]) == 1:
                return fetched[0][0]
            return fetched[0]
        if len(fetched) > 1 and len(fetched[0]) == 1:
            return [x[0] for x in fetched]
        return fetched

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
