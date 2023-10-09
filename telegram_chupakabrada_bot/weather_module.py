import os
from datetime import datetime

import requests
from connections import bot, MySQLUtils
from selects import simple_query, query


def weather_in_city_request(message):
    db_conn = MySQLUtils()
    if len(message.text.split(' ')) == 1:
        query(125, message.chat.id, db_conn)
    else:
        weather_in_city(message)


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


def weather(city_name: str) -> int:
    """
    Get current temperature
    :param city_name: city name or id
    :return: temp in Celsius
    """
    return int((requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&units=metric&appid={os.getenv('WEATHER_TOKEN')}"
    ).json())['main']['temp'])


def forecast(city: str) -> tuple:
    """
    Get forecast on today
    :param city: city name or id
    :return: temp on Celsius, conditions
    """
    response = requests.get(
        f"https://api.openweathermap.org/data/2.5/forecast?q={city}&lang=ru&units=metric&cnt=4&"
        f"appid={os.getenv('WEATHER_TOKEN')}"
    ).json()
    temp_celsius = int(response['list'][3]['main']['feels_like'])
    condition = response['list'][3]['weather'][0]['description'].lower()
    condition_emoji = {
        'ясно': '☀️',
        'небольшая облачность': '🌤',
        'облачно с прояснениями': '🌥',
        'пасмурно': '☁️',
        'небольшой дождь': '🌦',
        'переменная облачность': '⛅',
        'дождь': '🌨',
        'снег': '❄️',
        'небольшой снег': '🌨'
    }
    # ️⛈🌧🌦☁️🌥🌩🌨
    condition = condition_emoji[condition] if condition in condition_emoji else condition
    return temp_celsius, condition


def add_city_request(message):
    db_conn = MySQLUtils()
    if len(message.text.split(' ')) == 1:
        query(123, message.chat.id, db_conn)
    else:
        add_city(message)


def add_city(message):
    """
    Adds city to DB if this city really exists and send status to chat
    :param message: message from telegram
    :return: None
    """
    db_conn = MySQLUtils()
    chat_id = str(message.chat.id)
    city_name = message.text.split()
    city_name.pop(0)
    city_name = ' '.join(city_name).upper()
    # checking if city not exists
    try:
        weather(city_name)
        db_conn.mutate(f"insert into cities (chat_id, city_name) values ('{chat_id}', '{city_name}')")
        bot.send_message(message.chat.id, f'{city_name} {simple_query(121)}')
    except KeyError:
        bot.send_message(message.chat.id, f'{city_name}??? {simple_query(119)}')


def delete_city_request(message):
    db_conn = MySQLUtils()
    if len(message.text.split(' ')) == 1:
        query(124, message.chat.id, db_conn)
    else:
        delete_city(message)


def delete_city(message):
    """
    Deletes city from DB and send status to chat
    :param message: message from telegram
    :return: None
    """
    db_conn = MySQLUtils()
    chat_id = str(message.chat.id)
    city_name = message.text.split()
    city_name.pop(0)
    city_name = ' '.join(city_name).upper()
    try:
        records = db_conn.query(
            f"SELECT city_name FROM cities where upper(city_name)='{city_name}' and chat_id='{chat_id}';"
        )
        if len(records) != 0:
            try:
                db_conn.mutate(f"delete from cities where chat_id='{chat_id}' and upper(city_name)='{city_name}';")
                bot.send_message(message.chat.id, f'{city_name} {simple_query(126)}')
            except KeyError:
                pass
        else:
            bot.send_message(message.chat.id, simple_query(115))
    except KeyError:
        bot.send_message(message.chat.id, simple_query(115))


def add_temp_to_db(city_name: str, chat: int, db_conn: MySQLUtils):
    """
    Gets current and forecast temperatures, conditions and inserts it to DB
    :param city_name: city name or id
    :param chat: chat from telegram
    :param db_conn: connection to DB
    :return: None
    """
    expected, condition = forecast(city_name)
    db_conn.mutate(
        f"""update cities set temp={weather(city_name)}, expected_day_temp={expected}, conditions='{condition}'
            where city_name='{city_name}' and chat_id='{chat}';""")


def weather_send(chat_id, city_db, min_weather, max_weather, length, is_forecast, db_conn: MySQLUtils):
    """
    Checking max or min temp and places emoji near temp
    :param chat_id: chat id
    :param city_db: city name
    :param min_weather: min temperature from DB
    :param max_weather: max temperature from DB
    :param length: if length > 1 adds emoji
    :param is_forecast: selects from DB forecast or current weather
    :param db_conn: connection to DB
    :return:
    """
    fetched = db_conn.query(f"""select temp, expected_day_temp, conditions from cities
                    where chat_id='{chat_id}' and city_name='{city_db}';""")[0]
    temp = int(fetched[1]) if is_forecast else int(fetched[0])
    condition = fetched[2]
    if 0 <= temp < 10:
        temp_spaces = '  '
    elif (0 > temp > -10) or temp >= 10:
        temp_spaces = ' '
    else:
        temp_spaces = ''
    what_to_send = f"\n ` {temp_spaces}{temp}° {condition} {city_db}`"
    if length > 1:
        if temp == min_weather:
            what_to_send += ' 🥶️️'
        elif temp == max_weather:
            what_to_send += ' 🥵'
    return what_to_send


def get_weather_list(message):
    """getting cities list from DB."""
    if not isinstance(message, str):
        chat_id = message.chat.id
    else:
        chat_id = message
    db_conn = MySQLUtils()
    if datetime.now().hour in range(0, 7):
        weather_message = simple_query(128) + '\n'
        is_forecast = True
    else:
        weather_message = simple_query(122) + '\n'
        is_forecast = False
    fetched_from_db = db_conn.query(f"select city_name from cities where chat_id='{chat_id}';")
    # updating temperatures in DB
    for i in range(len(fetched_from_db)):
        city_db = str((fetched_from_db[i])[0])
        add_temp_to_db(city_db, chat_id, db_conn)
    # find max and min weather in cities list
    max_min_temp = 'expected_day_temp' if is_forecast else 'temp'
    if len(fetched_from_db) != 0:
        max_min_weather = db_conn.query(
            f"select max({max_min_temp}), min({max_min_temp}) from cities where chat_id='{chat_id}';"
        )[0]
        # getting each city and temp from db
        for i in range(len(fetched_from_db)):
            city_db = str((fetched_from_db[i])[0])
            weather_message += weather_send(chat_id, city_db, int(max_min_weather[1]), int(max_min_weather[0]),
                                            len(fetched_from_db), is_forecast, db_conn)
    else:
        weather_message = simple_query(116)
    bot.send_message(chat_id=chat_id, text=weather_message, parse_mode='Markdown')


if __name__ == '__main__':
    get_weather_list(os.getenv('HOME_TELEGA'))
