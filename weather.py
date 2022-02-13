import telebot
from conf import name, conn, go_weather
import psycopg2
import requests
from sys import argv

script, chat = argv
# connection to Bot
bot = telebot.TeleBot(name)
# connection to DB
conn_db = psycopg2.connect(conn)
cur = conn_db.cursor()


def weather(id: str) -> str:
    requestings = requests.get(
        'https://api.openweathermap.org/data/2.5/weather?q=' + id +
        (
             '&appid=' + go_weather
        )
    ).json()
    temp_farenheit = (requestings['main'])['temp']
    temp_celsius = str(int(temp_farenheit - 273))
    return temp_celsius


def add_temp_to_db(city_name, chat):
    temp = weather(city_name)
    cur.execute("update cities set temp=" + str(temp)
                + " where city_name='" + city_name
                + "' and chat_id='" + str(chat)
                + "'; ")
    conn_db.commit()


def weather_send(city_db, min_weather, max_weather, length):
    global what_to_send
    '''Checking max or min temp and send emoji near temp'''
    cur.execute("SELECT temp FROM cities where chat_id='"
                + str(chat) + "' and city_name='"
                + str(city_db) + "'; ")
    temp = int(str(cur.fetchall()).replace('[(', '').replace(',)]', ''))
    if temp >= 0 and temp < 10:
        temp_spaces = '  '
    elif (temp < 0 and int(temp) > -10) or temp > 10:
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


def get_weather_list(chat):
    global what_to_send
    what_to_send = (
        'Ну шо, с добрим утречком всех, мои зяблики, маи родненькие!\n\n'
        'Вот вам ваша пагода па расписанию, палучаица:\n')
    # getting cities list from DB
    cur.execute("SELECT city_name FROM cities "
                "where chat_id='" + str(chat) + "';")
    fetched_from_db = cur.fetchall()

    # updating temperatures in DB
    for i in range(0, len(fetched_from_db)):
        city_db = str(fetched_from_db[i]).replace("('", "").replace("',)", "")
        add_temp_to_db(city_db, chat)

    # find max and min weather in cities list
    if len(fetched_from_db) != 0:
        # max/min temp
        cur.execute("SELECT max(temp) FROM cities "
                    "where chat_id='" + str(chat) + "';")
        max_weather = int(
            str(cur.fetchall()).replace('[(', '').replace(',)]', ''))
        cur.execute("SELECT min(temp) FROM cities "
                    "where chat_id='" + str(chat) + "';")
        min_weather = int(
            str(cur.fetchall()).replace('[(', '').replace(',)]', ''))
        # parsing each city and temp from db
        for i in range(0, len(fetched_from_db)):
            city_db = str(
                fetched_from_db[i]).replace("('", "").replace("',)", "")
            weather_send(city_db,
                         min_weather,
                         max_weather,
                         len(fetched_from_db))

        bot.send_message(
            chat_id=chat,
            text=what_to_send,
            parse_mode='Markdown')
    else:
        bot.send_message(
            chat_id=chat,
            text='Так нету харадов!',
            parse_mode='Markdown')


get_weather_list(chat)
