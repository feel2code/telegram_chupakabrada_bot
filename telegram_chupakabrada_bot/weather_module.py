import os
from datetime import datetime
from typing import Optional

import requests

from connections import SQLUtils, bot
from selects import query, simple_query


def weather_in_city_request(message):
    if len(message.text.split(" ")) == 1:
        query(125, message.chat.id)
    else:
        weather_in_city(message)


def weather_in_city(message):
    """
    Constantly get temperature for any city without saving to DB and
    send weather to the chat
    :param message: message from telegram
    :return: None
    """
    city_name = message.text.replace("/weather ", "").replace(" ", "-")
    city_temp = weather(city_name)
    if not city_temp:
        bot.send_message(message.chat.id, simple_query(111))
        return
    bot.send_message(
        message.chat.id, f"{simple_query(112)}\n {city_temp} °C {city_name}"
    )


def weather(city_name: str) -> Optional[int]:
    """
    Get current temperature from db if exists else from API
    :param city_name: city name or id
    :return: temp in Celsius
    """
    db_conn = SQLUtils()
    if not db_conn.query(
        f"select city_name from cities where city_name='{city_name}';"
    ):
        db_conn.mutate(
            f"""insert into cities (
                city_name, temp, expected_day_temp, conditions, updated_at, is_active
                )
                values (
                '{city_name}', 0, 0, '', '{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', 0
                );"""
        )
    fetched_from_db = db_conn.query(
        f"select temp, updated_at from cities where city_name='{city_name}' and is_active=1;"
    )
    if fetched_from_db:
        city_temp, updated_at = fetched_from_db
        updated_at = datetime.strptime(updated_at, "%Y-%m-%d %H:%M:%S")
        if datetime.now().hour == updated_at.hour:
            return city_temp
    try:
        new_temp = int(
            (
                requests.get(
                    (
                        f"https://api.openweathermap.org/data/2.5/weather?q={city_name}"
                        f"&units=metric&appid={os.getenv('WEATHER_TOKEN')}"
                    ),
                    timeout=60,
                ).json()
            )["main"]["temp"]
        )
        db_conn.mutate(
            f"""update cities set temp={new_temp},
                updated_at='{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}',
                is_active=1
                where city_name='{city_name}';"""
        )
        return new_temp
    except KeyError as e:
        print(e)
        return None


def forecast(city: str) -> Optional[tuple]:
    """
    Get forecast on today from API
    :param city: city name or id
    :return: temp on Celsius, conditions
    """
    response = requests.get(
        (
            f"https://api.openweathermap.org/data/2.5/forecast?q={city}&"
            f"lang=ru&units=metric&cnt=4&appid={os.getenv('WEATHER_TOKEN')}"
        ),
        timeout=60,
    ).json()
    try:
        temp_celsius = int(response["list"][3]["main"]["feels_like"])
    except KeyError as e:
        print(e)
        return None
    condition = response["list"][3]["weather"][0]["description"].lower()
    condition_emoji = {
        "ясно": "☀️",
        "небольшая облачность": "🌤",
        "облачно с прояснениями": "🌥",
        "пасмурно": "☁️",
        "небольшой дождь": "🌦",
        "переменная облачность": "⛅",
        "дождь": "🌨",
        "снег": "❄️",
        "небольшой снег": "🌨",
        "сильный дождь": "🌧",
    }
    # ️⛈🌧🌦☁️🌥🌩🌨
    condition = (
        condition_emoji[condition] if condition in condition_emoji else condition
    )
    return temp_celsius, condition


def add_city_request(message):
    if len(message.text.split(" ")) == 1:
        query(123, message.chat.id)
    else:
        add_city(message)


def add_city(message):
    """
    Adds city to DB if this city really exists and send status to chat
    :param message: message from telegram
    :return: None
    """
    db_conn = SQLUtils()
    chat_id = message.chat.id
    city_name = message.text.split()
    city_name.pop(0)
    city_name = " ".join(city_name).upper()
    if not weather(city_name):
        bot.send_message(message.chat.id, f"{city_name}??? {simple_query(119)}")
    if db_conn.query(
        f"""select city_name from city_chat_id
            where upper(city_name)='{city_name}'
            and chat_id={chat_id};"""
    ):
        bot.send_message(message.chat.id, f"{city_name} {simple_query(121)}")
        return
    db_conn.mutate(
        f"""insert into city_chat_id (chat_id, city_name)
            values ({chat_id}, '{city_name}')"""
    )
    bot.send_message(message.chat.id, f"{city_name} {simple_query(121)}")


def delete_city_request(message):
    if len(message.text.split(" ")) == 1:
        query(124, message.chat.id)
    else:
        delete_city(message)


def delete_city(message):
    """
    Deletes city from DB and send status to chat
    :param message: message from telegram
    :return: None
    """
    db_conn = SQLUtils()
    chat_id = message.chat.id
    city_name = message.text.split()
    city_name.pop(0)
    city_name = " ".join(city_name).upper()
    try:
        records = db_conn.query(
            f"""SELECT city_name FROM city_chat_id
                where upper(city_name)='{city_name}'
                and chat_id={chat_id};"""
        )
        if len(records) != 0:
            try:
                db_conn.mutate(
                    f"""delete from city_chat_id
                        where chat_id={chat_id}
                        and upper(city_name)='{city_name}';"""
                )
                bot.send_message(message.chat.id, f"{city_name} {simple_query(126)}")
            except KeyError:
                pass
        else:
            bot.send_message(message.chat.id, simple_query(115))
    except KeyError:
        bot.send_message(message.chat.id, simple_query(115))


def add_temp_to_db(city_name: str, db_conn: SQLUtils):
    """
    Gets current and forecast temperatures, conditions and inserts it to DB
    :param city_name: city name or id
    :param chat: chat from telegram
    :param db_conn: connection to DB
    :return: None
    """
    updated_at = db_conn.query(
        f"select updated_at from cities where city_name='{city_name}';"
    )
    if updated_at:
        updated_at = datetime.strptime(updated_at, "%Y-%m-%d %H:%M:%S")
        if datetime.now().hour == updated_at.hour:
            return
    fetched_forecast = forecast(city_name)
    if fetched_forecast:
        expected, condition = fetched_forecast
        db_conn.mutate(
            f"""update cities set temp={weather(city_name)},
                expected_day_temp={expected}, conditions='{condition}'
                where city_name='{city_name}';"""
        )


def get_weather_list(message):
    """getting cities list from DB."""
    return_mode = False
    if not isinstance(message, str):
        chat_id = message.chat.id
    else:
        chat_id, return_mode = message, True
    if datetime.now().hour in range(0, 7):
        weather_message = simple_query(128) + "\n"
        is_forecast = True
    else:
        weather_message = simple_query(122) + "\n"
        is_forecast = False
    db_conn = SQLUtils()
    fetched_from_db = db_conn.query(
        f"select city_name from city_chat_id where chat_id={chat_id};"
    )
    if fetched_from_db:
        for city in fetched_from_db:
            add_temp_to_db(city, db_conn)
        temp_type = "expected_day_temp" if is_forecast else "temp"
        req = f"""
            select city_name, {temp_type}, conditions,
            (
            case when {temp_type}=(
                select max({temp_type})
                from cities
                where city_name in (select city_name from city_chat_id where chat_id={chat_id})
                )
            then ' 🥵'
            when {temp_type}=(
                select min({temp_type})
                from cities
                where city_name in ( select city_name from city_chat_id where chat_id={chat_id})
                )
            then ' 🥶️️'
            else ''
            end
            ) as min_max
            from cities
            where city_name in (
                select city_name from city_chat_id where chat_id={chat_id}
            );
        """
        fetched = db_conn.query(req)
        for row in fetched:
            city, temp, condition, add_cond = row
            if 0 <= temp < 10:
                temp_spaces = "  "
            elif (0 > temp > -10) or temp >= 10:
                temp_spaces = " "
            else:
                temp_spaces = ""
            weather_message += (
                f"\n ` {temp_spaces}{temp}° " f"{condition} {city}{add_cond}`"
            )
    else:
        weather_message = simple_query(116)
    if return_mode:
        return weather_message
    bot.send_message(chat_id=chat_id, text=weather_message, parse_mode="Markdown")
    return None
