import os
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from connections import bot, cur
from deprecation import deprecated


@deprecated()
def holiday(chat_id: str):
    """Все искажения грамматики неслучайны."""
    day = datetime.now().day
    month = datetime.now().month

    cur.execute(f"select month_name from months where id={month};")
    data = f'{day}_{cur.fetchone()[0]}'
    today = []
    page = requests.get(f'https://ru.wikipedia.org/wiki/Категория:Праздники_{data}')
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
        bot.send_message(chat_id=chat_id, text=f'Сиводня {datetime.now().date()}: \n{case}')
    except ValueError:
        bot.send_message(chat_id=chat_id, text=f'Сиводня {datetime.now().date()} праздников нет.')


def get_holidays(chat_id: str):
    """Gets full parsed list of holidays and sends to the specific chat."""
    # Все искажения грамматики неслучайны.
    holidays = []
    page = requests.get('https://calend.online/holiday/')
    if page.status_code == 200:
        holidays_list = BeautifulSoup(page.text, "html.parser").find('ul', class_='holidays-list')
        for one_holiday in holidays_list.select("li"):
            holidays.append(one_holiday.get_text().replace("\n", "").replace("  ", ""))
    holidays = "\n".join(holidays)
    bot.send_message(
        chat_id=chat_id,
        text=f'Сиводня {datetime.now().date()}:\n{holidays if holidays else "праздников нет."}'
    )


if __name__ == '__main__':
    # holiday(os.getenv('HOME_TELEGA')) # old method
    get_holidays(os.getenv('HOME_TELEGA'))
