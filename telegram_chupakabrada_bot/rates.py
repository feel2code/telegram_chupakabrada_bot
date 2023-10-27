import os

import json
import requests

from connections import MySQLUtils


def get_api_rates_and_insert():
    endpoint = ("http://api.exchangeratesapi.io/v1/latest?"
                f"access_key={os.getenv('RATES_TOKEN')}&symbols=USD,GEL,RUB")
    response = json.loads(requests.get(
        endpoint,
        timeout=5,
        headers={"user-agent": "Mozilla/80.0"}
    ))
    if response.success:
        rates = json.loads(response.text)['rates']
        db_conn = MySQLUtils()
        db_conn.mutate(
            "update rates set prev_rate=rate;"
        )
        db_conn.mutate(
            f"""insert into rates (ccy_iso3, rate)
            values {str(tuple(rates.items()))[1:-1]}"""
        )


if __name__ == '__main__':
    get_api_rates_and_insert()
