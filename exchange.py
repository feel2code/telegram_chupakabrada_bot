import telebot
from bs4 import BeautifulSoup
from conf import db_name, bot_token, home_telega
import psycopg2
import requests
import time
import logging


connection_to_db = psycopg2.connect(db_name)
cursor = connection_to_db.cursor()
logging.basicConfig(
    level=logging.DEBUG,
    filename='exchange.log',
    format=(
        '%(asctime)s - %(module)s - %(levelname)s'
        ' - %(funcName)s: %(lineno)d - %(message)s'
    ),
    datefmt='%H:%M:%S',
)


def get_usd_course():
    page = requests.get('https://quote.rbc.ru/ticker/59111')
    time.sleep(10)
    soup = BeautifulSoup(page.text, "html.parser")
    data = soup.find(
        'div', class_='chart__info__row js-ticker'
    ).find(
        'span', class_='chart__info__sum'
    ).text
    float_rate = float(
        data.replace('₽', '').replace(' ', '').replace(',', '.')
    )
    int_rate = int(float_rate)
    rate_remain = float_rate - int_rate
    if int(rate_remain * 10) in range(0, 4) or rate_remain in range(8, 10):
        return int_rate
    else:
        return None


def check_course():
    rate = get_usd_course()
    if rate is not None:
        cursor.execute(
            "select course_value from course where course_name='usd'; "
        )
        last_rate = cursor.fetchone()[0]
        if rate != last_rate:
            cursor.execute(
                f"update course set course_value={rate} "
                f"where course_name='usd'; "
            )
            connection_to_db.commit()
            bot = telebot.TeleBot(bot_token)
            bot.send_message(
                chat_id=home_telega,
                text=f'Далар уже па {rate} ₽'
            )
        else:
            pass
    else:
        pass


while True:
    check_course()
    time.sleep(50)
