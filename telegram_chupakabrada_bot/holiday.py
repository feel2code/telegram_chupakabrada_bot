import os
from datetime import datetime

from calendar import Calendar, MONDAY
import requests
from bs4 import BeautifulSoup

from connections import bot, MySQLUtils


def get_holidays_from_db(chat_id: str):
    """Get holidays from db."""
    # Все искажения грамматики неслучайны.
    # get week and day from calendar to check relative holidays
    db_conn = MySQLUtils()
    month_calendar = Calendar(firstweekday=MONDAY).monthdatescalendar(datetime.utcnow().year, datetime.utcnow().month)
    day_num, week_num = 0, 0
    for week_idx, week in enumerate(month_calendar):
        for day_idx, day in enumerate(week):
            if day == datetime.today().date():
                day_num, week_num = day_idx + 1, week_idx  # monday = 1, tuesday = 2 etc.
                break
    # get current day and month
    day, month = datetime.now().day, datetime.now().month
    fetched = db_conn.query(
                f"""select * from (
                    (select holiday_name from (
                        select
                            cast(extract(day from dt) as unsigned) as day,
                            cast(extract(month from dt) as unsigned) as month,
                            concat('🇷🇺 ', holiday_name) as holiday_name from holidays_ru hr
                        union all
                        select
                            cast(extract(day from dt) as unsigned) as day,
                            cast(extract(month from dt) as unsigned) as month,
                            concat('🌍 ', holiday_name) as holiday_name from holidays_iso iso
                        ) as holidays
                    where day={day} and month={month})
                    union all (
                        select concat('🇷🇺 ', holiday_name) as holiday_name
                        from holidays_ru_relative hrr
                        where day_num={day_num} and week_num={week_num} and extract(month from dt)={month}
                    )) as holidays_all;""")
    fetched = [x[0] for x in fetched]
    holidays_from_db = '\n'.join(fetched) if fetched else 'Сиводня праздников нет! Пойду сделаю омлет...'
    message = f'Хааай, пасики! Сиводня палучаица {datetime.now().date()}:\n\n' + holidays_from_db
    bot.send_message(chat_id=chat_id, text=message)


def get_wiki_holiday(chat_id: str):
    """Get list of holidays including links to wiki."""
    # Все искажения грамматики неслучайны.
    db_conn = MySQLUtils()
    day, month = datetime.now().day, datetime.now().month
    month_ru = db_conn.query(f"select month_name from months where id={month};")[0][0]
    holidays_list = []
    wiki_host = 'https://ru.wikipedia.org/'
    page = requests.get(f'{wiki_host}wiki/Категория:Праздники_{day}_{month_ru}')
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
    get_holidays_from_db(os.getenv('HOME_TELEGA'))
