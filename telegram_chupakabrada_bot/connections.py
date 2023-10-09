import os

import mysql.connector as mysql_conn
import telebot
from dotenv import load_dotenv
from mysql.connector.errors import DatabaseError, OperationalError

load_dotenv(".env")
bot = telebot.TeleBot(os.getenv('BOT_TOKEN'))


class MySQLUtils:
    conn = None

    def connect(self):
        self.conn = mysql_conn.connect(user=os.getenv('DB_USER'),
                                       password=os.getenv('DB_PASSWORD'),
                                       host=os.getenv('DB_HOST'),
                                       database=os.getenv('DB_NAME'))

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
