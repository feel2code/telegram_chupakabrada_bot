import json
import os

import requests
import telebot

from connections import SQLUtils


def get_api_rates_and_insert():
    endpoint = (
        "http://api.exchangeratesapi.io/v1/latest?"
        f"access_key={os.getenv('RATES_TOKEN')}&symbols=USD,GEL,RUB"
    )
    response = json.loads(
        requests.get(endpoint, timeout=5, headers={"user-agent": "Mozilla/80.0"}).text
    )
    if response["success"]:
        rates = response["rates"]
        db_conn = SQLUtils()
        db_conn.mutate("update rates set prev_rate=rate;")
        for ccy, val in rates.items():
            db_conn.mutate(f"update rates set rate={val} where ccy_iso3='{ccy}';")


def check_usd_rate_change():
    """Искажения грамматики неслучайны."""
    db_conn = SQLUtils()
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
        bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))
        bot.send_message(
            chat_id=os.getenv("HOME_TELEGA"), text=f"Далар уже па {rate} ₽"
        )


if __name__ == "__main__":
    get_api_rates_and_insert()
    check_usd_rate_change()
