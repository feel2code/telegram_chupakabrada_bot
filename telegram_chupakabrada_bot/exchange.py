import os
import time
from typing import Union

import json
import requests
import telebot
from bs4 import BeautifulSoup

from connections import MySQLUtils


def check_usd_rate_change():
    """Искажения грамматики неслучайны."""
    db_conn = MySQLUtils()
    rates = db_conn.query(
        """select
	    round((
         select rate / (select rate from rates
         where ccy_iso3 = 'USD') from rates where ccy_iso3 = 'RUB'
        ), 1) as rate,
	    round((
         select prev_rate / (select prev_rate from rates
         where ccy_iso3 = 'USD') from rates where ccy_iso3 = 'RUB'
        ), 1) as prev_rate;"""
    )[0]
    rate, prev_rate = [int(x) for x in rates]
    if rate != prev_rate:
        bot = telebot.TeleBot(os.getenv('BOT_TOKEN'))
        bot.send_message(chat_id=os.getenv('HOME_TELEGA'),
                         text=f'Далар уже па {rate} ₽')


if __name__ == '__main__':
    check_usd_rate_change()
