import logging
import os
import time
from typing import Union

import requests
import telebot
from bs4 import BeautifulSoup

from connections import conn_db, cur


logging.basicConfig(
    level=logging.DEBUG,
    filename=f"{'/'.join(os.getcwd().split('/')[:-1])}/exchange.log",
    format=(
        '%(asctime)s - %(module)s - %(levelname)s'
        ' - %(funcName)s: %(lineno)d - %(message)s'
    ),
    datefmt='%H:%M:%S',
)


def get_usd_course() -> Union[int, None]:
    url = 'https://www.bloomberg.com/quote/USDRUB:CUR'
    time.sleep(10)
    response = requests.get(url, timeout=5, headers={"user-agent": "Mozilla/80.0"})
    soup = BeautifulSoup(response.text, "html.parser")
    rate = float(soup.find('div', class_='overviewRow__ab9704fa12').find('span', class_='priceText__0550103750').text)
    rate_remain = rate - int(rate)
    if int(rate_remain * 10) in range(0, 4) or rate_remain in range(8, 10):
        return int(rate)
    return None


def get_gel_course() -> Union[int, None]:
    url = 'https://www.xe.com/currencyconverter/convert/?Amount=1&From=GEL&To=RUB'
    time.sleep(10)
    response = requests.get(url, timeout=5, headers={"user-agent": "Mozilla/80.0"})
    soup = BeautifulSoup(response.text, "html.parser")
    return int(float(soup.find('p', class_='result__BigRate-sc-1bsijpp-1 iGrAod').text.split()[0]))


def check_course():
    """Искажения грамматики неслучайны."""
    rate, gel_rate = get_usd_course(), get_gel_course()
    cur.execute(f"update course set course_value={gel_rate} where course_name='gel';")
    conn_db.commit()
    if rate is not None:
        cur.execute("select course_value from course where course_name='usd';")
        last_rate = cur.fetchone()[0]
        if rate != last_rate:
            cur.execute(f"update course set course_value={rate} where course_name='usd';")
            conn_db.commit()
            bot = telebot.TeleBot(os.getenv('BOT_TOKEN'))
            bot.send_message(chat_id=os.getenv('HOME_TELEGA'), text=f'Далар уже па {rate} ₽')
        else:
            pass
    else:
        pass


if __name__ == '__main__':
    while True:
        check_course()
        time.sleep(120)
