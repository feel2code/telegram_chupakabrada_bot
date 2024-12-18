from calendar import MONDAY, Calendar
from datetime import date, datetime

import requests
from bs4 import BeautifulSoup

from connections import SQLUtils, bot


def is_date_is_last_weekday_of_month(checking_date: date, weekday: int) -> int:
    """Check if the date is the last weekday of the month."""
    month_calendar = Calendar(firstweekday=MONDAY).monthdayscalendar(
        checking_date.year, checking_date.month
    )
    months_weekdays = [week[weekday] for week in month_calendar if week[weekday] != 0]
    return int(checking_date.day == months_weekdays[-1])


def current_weekday_counter_in_month(check_date: date):
    """Returns current weekday counter in month."""
    return sum(
        1
        for i in range(1, check_date.day + 1)
        if date(check_date.year, check_date.month, i).weekday() == check_date.weekday()
    )


def get_holidays_from_db(message):
    """Get holidays from db."""
    # Все искажения грамматики неслучайны.
    return_mode = False
    if not isinstance(message, str):
        chat_id = message.chat.id
    else:
        chat_id, return_mode = message, True
    db_conn = SQLUtils()
    # get week and day from calendar to check relative holidays
    cur_day = datetime.today().day
    cur_month = datetime.today().month
    cur_weekday = datetime.today().weekday()
    weekday_counter = current_weekday_counter_in_month(datetime.today())
    is_last = is_date_is_last_weekday_of_month(datetime.today(), cur_weekday)

    additional_condition = (
        f"and week_num={weekday_counter}" if not is_last else f"and is_last={is_last}"
    )
    fetched = db_conn.query(
        f"""with base_holidays as (
            select holiday_name from (
                        select
                            cast(strftime('%d', dt) as integer) as day,
                            cast(strftime('%m', dt) as integer) as month,
                            '🇷🇺 ' || holiday_name as holiday_name
                        from holidays_ru hr
                        union all
                        select
                            cast(strftime('%d', dt) as integer) as day,
                            cast(strftime('%m', dt) as integer) as month,
                            '🌍 ' || holiday_name as holiday_name
                        from holidays_iso iso
                        ) as holidays
                    where day={cur_day} and month={cur_month}
            ),
            relative_holidays as (
                select 
                    '🇷🇺 ' || holiday_name as holiday_name
                from holidays_ru_relative hrr
                where day_num={cur_weekday + 1}
                and cast(strftime('%m', dt) as integer)={cur_month}
                {additional_condition}
            )
                select * from base_holidays
                union all
                select * from relative_holidays;"""
    )
    if fetched:
        if isinstance(fetched, list):
            holidays_from_db = "\n".join(fetched)
        else:
            holidays_from_db = fetched
    else:
        holidays_from_db = "Сиводня праздников нет! Пойду сделаю омлет..."
    if return_mode:
        return holidays_from_db
    bot.send_message(
        chat_id=chat_id,
        text=(
            f"Хааай, пасики! Сиводня палучаица {datetime.now().date()}:\n\n{holidays_from_db}"
        ),
    )
    return None


def get_wiki_holiday(message):
    """Get list of holidays including links to wiki."""
    # Все искажения грамматики неслучайны.
    db_conn = SQLUtils()
    day, month = datetime.now().day, datetime.now().month
    month_ru = db_conn.query(f"select month_name from months where id={month};")
    holidays_list = []
    wiki_host = "https://ru.wikipedia.org/"
    page = requests.get(
        f"{wiki_host}wiki/Категория:Праздники_{day}_{month_ru}", timeout=60
    )
    try:
        holidays = BeautifulSoup(page.text, "html.parser").find(
            "div", class_="mw-category"
        )
        for item in holidays.select("li"):
            link = wiki_host + item.find("a").get("href").replace(")", "%29")
            title = item.find("a").get_text()
            holidays_list.append(f"[{title}]({link})")
        answer = (
            f"Хааай, пасики! Сиводня палучаица {datetime.now().date()}:\n"
            + "\n".join(holidays_list)
        )
        bot.send_message(chat_id=message.chat.id, text=answer, parse_mode="Markdown")
    except (ValueError, AttributeError) as e:
        print(e)
        bot.send_message(
            chat_id=message.chat.id,
            text=f"На сиводня {datetime.now().date()} праздников нет.",
        )


def get_holidays(chat_id: str):
    """Gets full parsed list of holidays and sends to the specific chat."""
    # Все искажения грамматики неслучайны.
    holidays = []
    page = requests.get("https://calend.online/holiday/", timeout=60)
    if page.status_code == 200:
        holidays_list = BeautifulSoup(page.text, "html.parser").find(
            "ul", class_="holidays-list"
        )
        for one_holiday in holidays_list.select("li"):
            holidays.append(one_holiday.get_text().replace("\n", "").replace("  ", ""))
    holidays_result = "\n".join(holidays)
    bot.send_message(
        chat_id=chat_id,
        text=(
            f"Сиводня {datetime.now().date()}:\n"
            f'{holidays_result if holidays_result else "праздников нет."}'
        ),
    )
