from datetime import datetime

import requests
from bs4 import BeautifulSoup

from connections import bot, cur


def holiday(chat_id):
    day = datetime.now().day
    month = datetime.now().month

    cur.execute(f"SELECT month_name FROM months where id={month}; ")
    fetched_month_name = cur.fetchone()[0]
    data = f'{day}_{fetched_month_name}'
    today = []
    page = requests.get(
        f'https://ru.wikipedia.org/wiki/Категория:Праздники_{data}'
    )

    soup = BeautifulSoup(page.text, "html.parser")
    for item in soup.select("li"):
        today.append(item.get_text())
    try:
        index = today.index('Праздники' + data.replace(str(day) + '_', ' '))
        i = index
        while len(today) != i:
            today.pop(index)
        today[0] = ' ' + today[0]
        case = str([word + '\n' for word in today]).replace(
            ',', '').replace('[', '').replace(']', '').replace(
            '[', '').replace("'", "").replace(r"\n", "\n")
        bot.send_message(
            chat_id=chat_id,
            text=f'Сиводня {datetime.now().date()}: \n{case}'
        )
    except ValueError:
        bot.send_message(
            chat_id=chat_id,
            text=f'Сиводня {datetime.now().date()} праздников нет.'
        )
