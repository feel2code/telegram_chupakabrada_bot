from calendar import MONDAY, Calendar
from datetime import datetime, timezone

import requests
from bs4 import BeautifulSoup

from connections import SQLUtils, bot


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
    month_calendar = Calendar(firstweekday=MONDAY).monthdayscalendar(
        datetime.now(timezone.utc).year, cur_month
    )
    months_weekdays = [
        week[cur_weekday] for week in month_calendar if week[cur_weekday] != 0
    ]
    day_idx = months_weekdays.index(cur_day) + 1
    is_last = 1 if months_weekdays[-1] == cur_day else 0
    additional_condition = (
        f"and week_num={day_idx}" if not is_last else f"and is_last={is_last}"
    )
    fetched = [
        x[0]
        for x in db_conn.query(
            f"""select * from (
                    (select holiday_name from (
                        select
                            cast(extract(day from dt) as unsigned) as day,
                            cast(extract(month from dt) as unsigned) as month,
                            concat('🇷🇺 ', holiday_name) as holiday_name
                        from holidays_ru hr
                        union all
                        select
                            cast(extract(day from dt) as unsigned) as day,
                            cast(extract(month from dt) as unsigned) as month,
                            concat('🌍 ', holiday_name) as holiday_name
                        from holidays_iso iso
                        ) as holidays
                    where day={cur_day} and month={cur_month})
                    union all (
                        select concat('🇷🇺 ', holiday_name) as holiday_name
                        from holidays_ru_relative hrr
                        where day_num={cur_weekday + 1}
                              and extract(month from dt)={cur_month}
                        {additional_condition}
                    )) as holidays_all;"""
        )
    ]
    holidays_from_db = (
        "\n".join(fetched)
        if fetched
        else "Сиводня праздников нет! Пойду сделаю омлет..."
    )
    if return_mode:
        return holidays_from_db
    bot.send_message(
        chat_id=chat_id,
        text=(
            f"Хааай, пасики! Сиводня палучаица {datetime.now().date()}:\n\n"
            + holidays_from_db
        ),
    )
    return None


def get_wiki_holiday(message):
    """Get list of holidays including links to wiki."""
    # Все искажения грамматики неслучайны.
    db_conn = SQLUtils()
    day, month = datetime.now().day, datetime.now().month
    month_ru = db_conn.query(f"select month_name from months where id={month};")[0][0]
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
