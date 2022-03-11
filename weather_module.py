import requests
from datetime import datetime

from conf import weather_token
from connections import bot, conn_db, cur
from selects import simple_query
from constants import TEMPERATURE_NOT_EXIST


def weather_in_city(message):
    city = message.text.replace('/weather ', '').replace(' ', '-')
    try:
        req = requests.get(
            'https://api.openweathermap.org/data/2.5/weather?q=' + city
            + '&appid=' + weather_token).json()
        city_temp = str(int((req['main'])['temp'] - 273))
        what_to_send = simple_query(112)
        what_to_send += ('\n ' + city_temp + ' °C ' + city)
    except KeyError:
        what_to_send = simple_query(111)
    bot.send_message(message.chat.id, what_to_send)


def weather(id: str) -> str:
    requestings = requests.get(
        f'https://api.openweathermap.org/data/2.5/'
        f'weather?q={id}&appid={weather_token}'
    ).json()
    temp_celsius = str(int((requestings['main'])['temp'] - 273))
    return temp_celsius


def add_city(message):
    chat_id = str(message.chat.id)
    city_name = str(
        message.text).replace('/add ', '').replace(' ', '-').upper()
    # checking if city not exists
    try:
        requestings = requests.get(
            'https://api.openweathermap.org/data/2.5/weather?q=' + city_name +
            (
                '&appid=' + weather_token
            )
        ).json()
        temp_farenheit = (requestings['main'])['temp']
        temp_celsius_test = str(int(temp_farenheit - 273))
    except KeyError:
        temp_celsius_test = TEMPERATURE_NOT_EXIST
    if temp_celsius_test != TEMPERATURE_NOT_EXIST:
        cur.execute("insert into cities (chat_id, city_name) "
                    "values (%s, %s)", (chat_id, city_name))
        conn_db.commit()
        what_to_send = city_name + ' ' + simple_query(121)
    else:
        what_to_send = simple_query(119)
    bot.send_message(message.chat.id, what_to_send)


def delete_city(message):
    chat_id = str(message.chat.id)
    city_name = message.text.replace('/delete ', '').replace(' ', '-').upper()
    try:
        cur.execute(
            "SELECT city_name FROM cities where"
            " upper(city_name)='" + city_name + "'; ")
        records = str(cur.fetchall())
        if records != '[]':
            try:
                cur.execute("delete from cities where chat_id='" + chat_id
                            + "' and upper(city_name)='" + city_name + "';")
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
    temp = weather(city_name)
    cur.execute("update cities set temp=" + str(temp)
                + " where city_name='" + city_name
                + "' and chat_id='" + str(chat)
                + "'; ")
    conn_db.commit()


def weather_send(chat_id, city_db, min_weather, max_weather, length):
    global what_to_send
    '''Checking max or min temp and send emoji near temp'''
    cur.execute("SELECT temp FROM cities where chat_id='"
                + str(chat_id) + "' and city_name='"
                + str(city_db) + "'; ")
    temp = int(cur.fetchone()[0])
    if temp >= 0 and temp < 10:
        temp_spaces = '  '
    elif (temp < 0 and int(temp) > -10) or temp >= 10:
        temp_spaces = ' '
    else:
        temp_spaces = ''
    what_to_send += (
        "\n ` " + temp_spaces + str(temp) + "° · " + city_db + " `")
    if length > 1:
        if temp == min_weather:
            what_to_send += ' ❄️'
        elif temp == max_weather:
            what_to_send += ' 🔥'


def get_weather_list(chat_id):
    global what_to_send
    if datetime.now().hour in range(0, 7):
        what_to_send = simple_query(128) + '\n\n'
    else:
        what_to_send = ''
    what_to_send += simple_query(122) + '\n'
    # getting cities list from DB
    cur.execute("SELECT city_name FROM cities "
                "where chat_id='" + str(chat_id) + "';")
    fetched_from_db = cur.fetchall()

    # updating temperatures in DB
    for i in range(0, len(fetched_from_db)):
        city_db = str((fetched_from_db[i])[0])
        add_temp_to_db(city_db, chat_id)

    # find max and min weather in cities list
    if len(fetched_from_db) != 0:
        # max/min temp
        cur.execute("SELECT max(temp) FROM cities "
                    "where chat_id='" + str(chat_id) + "';")
        max_weather = int((cur.fetchall()[0])[0])
        cur.execute("SELECT min(temp) FROM cities "
                    "where chat_id='" + str(chat_id) + "';")
        min_weather = int((cur.fetchall()[0])[0])
        # parsing each city and temp from db
        for i in range(0, len(fetched_from_db)):
            city_db = str((fetched_from_db[i])[0])
            weather_send(chat_id,
                         city_db,
                         min_weather,
                         max_weather,
                         len(fetched_from_db))
    else:
        what_to_send = simple_query(116)
    bot.send_message(
        chat_id=chat_id,
        text=what_to_send,
        parse_mode='Markdown')
