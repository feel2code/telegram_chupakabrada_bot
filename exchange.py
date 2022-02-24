import telebot
from bs4 import BeautifulSoup
from conf import db_name, bot_token, home_telega
import psycopg2
import requests
import time

connection_to_db = psycopg2.connect(db_name)
cursor = connection_to_db.cursor()


def get_usd_course():
    page = requests.get('https://quote.rbc.ru/ticker/59111')
    time.sleep(2)
    soup = BeautifulSoup(page.text, "html.parser")
    data = soup.find(
        'div', class_='chart__info__row js-ticker'
        ).find('span', class_='chart__info__sum').text
    data = data.replace('₽', '').replace(' ', '').replace(',', '.')
    rate = int(float(data))
    return rate


def check_course():
    rate = get_usd_course()
    cursor.execute("select course_value from course where course_name='usd'; ")
    last_rate = cursor.fetchone()[0]
    if rate != last_rate:
        cursor.execute(
            f"update course set course_value={rate} where course_name='usd'; "
        )
        connection_to_db.commit()
        bot = telebot.TeleBot(bot_token)
        bot.send_message(chat_id=home_telega, text=f'Далар уже па {rate} руб.')
    else:
        pass


while True:
    check_course()
    time.sleep(10)
