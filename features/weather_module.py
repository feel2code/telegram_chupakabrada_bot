from datetime import datetime

import requests

from conf import weather_token
from connections import bot, conn_db, cur
from constants import TEMPERATURE_NOT_EXIST
from selects import simple_query


def weather_in_city(message):
    """
    Constantly get temperature for any city without saving to DB and send weather to chat
    :param message: message from telegram
    :return: None
    """
    city_name = message.text.replace('/weather ', '').replace(' ', '-')
    try:
        city_temp = weather(city_name)
        bot.send_message(message.chat.id, f'{simple_query(112)}\n {city_temp} °C {city_name}')
    except KeyError:
        bot.send_message(message.chat.id, simple_query(111))


def weather(city_name: str) -> str:
    """
    Get current temperature
    :param city_name: city name or id
    :return: temp in Celsius
    """
    response = requests.get(
        f'https://api.openweathermap.org/data/2.5/'
        f'weather?q={city_name}&appid={weather_token}'
    ).json()
    temp_celsius = str(int((response['main'])['temp'] - 273))
    return temp_celsius


def forecast(city_name: str) -> tuple:
    """
    Get forecast on today
    :param city_name: city name or id
    :return: temp on Celsius, conditions
    """
    response = requests.get(
        f'https://api.openweathermap.org/data/2.5/'
        f'forecast?q={city_name}&lang=ru&appid={weather_token}'
    ).json()
    temp_celsius = str(int((response['list'][0]['main']['feels_like']) - 273))
    condition = response['list'][0]['weather'][0]['description'].lower()
    condition_emoji = {
        'ясно': '☀️',
        'небольшая облачность': '🌤',
        'облачно с прояснениями': '🌥',
        'пасмурно': '☁️',
        'небольшой дождь': '🌦',
        'переменная облачность': '⛅'
    }
    # ☀️🌤⛅️⛈🌧🌦☁️🌥🌩🌨❄️
    condition = condition_emoji[condition] if condition in condition_emoji else condition
    return temp_celsius, condition


def add_city(message):
    """
    Adds city to DB if this city really exists and send status to chat
    :param message: message from telegram
    :return: None
    """
    chat_id = str(message.chat.id)
    city_name = str(
        message.text).replace('/add ', '').replace(' ', '-').upper()
    # checking if city not exists
    try:
        temp_celsius_test = weather(city_name)
    except KeyError:
        temp_celsius_test = TEMPERATURE_NOT_EXIST
    if temp_celsius_test != TEMPERATURE_NOT_EXIST:
        cur.execute("insert into cities (chat_id, city_name) "
                    "values (%s, %s)", (chat_id, city_name))
        conn_db.commit()
        bot.send_message(message.chat.id, f'{city_name} {simple_query(121)}')
    else:
        bot.send_message(message.chat.id, simple_query(119))


def delete_city(message):
    """
    Deletes city from DB and send status to chat
    :param message: message from telegram
    :return: None
    """
    chat_id = str(message.chat.id)
    city_name = message.text.replace('/delete ', '').replace(' ', '-').upper()
    try:
        cur.execute(
            f"SELECT city_name FROM cities where"
            f" upper(city_name)='{city_name}'; "
        )
        records = str(cur.fetchall())
        if records != '[]':
            try:
                cur.execute(
                    f"delete from cities where chat_id='{chat_id}' and "
                    f"upper(city_name)='{city_name}';"
                )
                conn_db.commit()
                what_to_send = city_name + ' ' + simple_query(126)
                bot.send_message(message.chat.id, what_to_send)
            except KeyError:
                pass
        else:
            bot.send_message(message.chat.id, simple_query(115))
    except KeyError:
        bot.send_message(message.chat.id, simple_query(115))


def add_temp_to_db(city_name, chat):
    """
    Gets current and forecast temperatures, conditions and inserts it to DB
    :param city_name: city name or id
    :param chat: chat from telegram
    :return: None
    """
    temp = weather(city_name)
    expected, condition = forecast(city_name)
    cur.execute(f"""update cities
                    set temp={temp}, expected_day_temp={expected},
                        condition='{condition}'
                    where city_name='{city_name}' and chat_id='{chat}';""")
    conn_db.commit()


def weather_send(chat_id, city_db, min_weather, max_weather, length, is_forecast):
    """
    Checking max or min temp and places emoji near temp
    :param chat_id: chat id
    :param city_db: city name
    :param min_weather: min temperature from DB
    :param max_weather: max temperature from DB
    :param length: if length > 1 adds emoji
    :param is_forecast: selects from DB forecast or current weather
    :return:
    """
    cur.execute(
        f"""SELECT temp, expected_day_temp, condition
            FROM cities
            where chat_id='{chat_id}' and city_name='{city_db}';"""
    )
    fetched = cur.fetchall()[0]
    temp = int(fetched[1]) if is_forecast else int(fetched[0])
    condition = fetched[2]
    if 0 <= temp < 10:
        temp_spaces = '  '
    elif (temp < 0 and int(temp) > -10) or temp >= 10:
        temp_spaces = ' '
    else:
        temp_spaces = ''
    what_to_send = f"\n ` {temp_spaces}{temp}° {condition} {city_db}`"
    if length > 1:
        if temp == min_weather:
            what_to_send += '- 🥶️️'
        elif temp == max_weather:
            what_to_send += '- 🥵'
    return what_to_send


def get_weather_list(chat_id):
    """getting cities list from DB."""
    if datetime.now().hour in range(0, 7):
        weather_message = simple_query(128) + '\n'
        is_forecast = True
    else:
        weather_message = simple_query(122) + '\n'
        is_forecast = False
    cur.execute(
        f"SELECT city_name FROM cities "
        f"where chat_id='{chat_id}';"
    )
    fetched_from_db = cur.fetchall()
    # updating temperatures in DB
    for i in range(len(fetched_from_db)):
        city_db = str((fetched_from_db[i])[0])
        add_temp_to_db(city_db, chat_id)
    # find max and min weather in cities list
    max_min_temp = 'expected_day_temp' if is_forecast else 'temp'
    if len(fetched_from_db) != 0:
        cur.execute(
            f"""SELECT max({max_min_temp}), min({max_min_temp})
                FROM cities
                where chat_id='{chat_id}';"""
        )
        max_min_weather = cur.fetchall()[0]
        # getting each city and temp from db
        for i in range(len(fetched_from_db)):
            city_db = str((fetched_from_db[i])[0])
            weather_message += weather_send(chat_id,
                                            city_db,
                                            int(max_min_weather[1]),
                                            int(max_min_weather[0]),
                                            len(fetched_from_db),
                                            is_forecast)
    else:
        weather_message = simple_query(116)
    bot.send_message(
        chat_id=chat_id,
        text=weather_message,
        parse_mode='Markdown')
