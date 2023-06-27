import os
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from connections import bot, cur


def get_wiki_holiday(chat_id: str):
    """Get list of holidays including links to wiki."""
    # Все искажения грамматики неслучайны.
    day, month = datetime.now().day, datetime.now().month
    cur.execute(f"select month_name from months where id={month};")
    holidays_list = []
    wiki_host = 'https://ru.wikipedia.org/'
    page = requests.get(f'{wiki_host}wiki/Категория:Праздники_{day}_{cur.fetchone()[0]}')
    try:
        holidays = BeautifulSoup(page.text, "html.parser").find('div', class_='mw-category')
        for item in holidays.select("li"):
            link = wiki_host + item.find('a').get('href').replace(')', '%29')
            title = item.find('a').get_text()
            holidays_list.append(f'[{title}]({link})')
        message = f'Хааай, пасики! Сиводня палучаица {datetime.now().date()}:\n' + '\n'.join(holidays_list)
        bot.send_message(chat_id=chat_id, text=message, parse_mode='Markdown')
    except ValueError:
        bot.send_message(chat_id=chat_id, text=f'На сиводня {datetime.now().date()} праздников нет.')


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
    get_wiki_holiday(os.getenv('HOME_TELEGA'))
