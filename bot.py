import telebot
from conf import name, conn, go_weather, key_for_stats
import random
import psycopg2
import os
from datetime import datetime
import time
import requests
from hru import hru_list

# connection to Bot
bot = telebot.TeleBot(name)

# connection to DB
conn_db = psycopg2.connect(conn)
cur = conn_db.cursor()


# checking does message has any word in list from dictionary
def check(message):
    msg_check = message.text.upper().split()
    b = len(msg_check)
    i = 0
    while i < b:
        quest = msg_check[i]
        try:
            cur.execute(r"SELECT a.answer FROM questions as q join answers a "
                        r"on q.ans_id=a.ans_id where upper(q.question)='"
                        + quest + "' ")
            records = cur.fetchall()
            rec = (str(records[0]).replace("('", "")).replace("',)", "")
            if rec == '3 4 5 0 D':
                rec = ''
                query(103, message)
                time.sleep(1)
                i_count = 104
                while i_count < 111:
                    query(i_count, message)
                    time.sleep(0.100)
                    i_count += 1
                i_count = 109
                while i_count > 103:
                    query(i_count, message)
                    time.sleep(0.100)
                    i_count = i_count - 1
                i += 1
            else:
                bot.send_message(message.chat.id, rec)
                i += 1
        except IndexError:
            i += 1


# query from db, get answer to send
def query(ans_id, message):
    cur.execute("SELECT answer FROM answers where ans_id=" + str(ans_id) + " ")
    records = cur.fetchall()
    rec = (str(records[0]).replace("('", "")
           ).replace("',)", "").replace(")", "")
    bot.send_message(message.chat.id, rec)


def get_city_name(message):
    city = message.text.replace('/weather ', '').replace(' ', '-')
    try:
        req = requests.get(
            'https://api.openweathermap.org/data/2.5/weather?q=' + city
            + '&appid=' + go_weather).json()
        city1 = req['main']
        city_temp = str(int(city1['temp'] - 273))
        cur.execute("SELECT answer FROM answers where ans_id=112")
        records = cur.fetchall()
        what_to_send = (str(records[0]).replace("('", "")
                        ).replace("',)", "").replace(")", "")
        what_to_send += ('\n ' + city_temp + ' °C ' + city)
    except KeyError:
        cur.execute("SELECT answer FROM answers where ans_id=111")
        records = cur.fetchall()
        what_to_send = (str(records[0]).replace("('", "")
                        ).replace("',)", "").replace(")", "")
    bot.send_message(message.chat.id, what_to_send)


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


def add_city(message):
    chat_id = str(message.chat.id)
    city_name = str(
        message.text).replace('/add ', '').replace(' ', '-').upper()
    # checking if city not exists
    try:
        requestings = requests.get(
            'https://api.openweathermap.org/data/2.5/weather?q=' + city_name +
            (
                '&appid=' + go_weather
            )
        ).json()
        temp_farenheit = (requestings['main'])['temp']
        temp_celsius_test = str(int(temp_farenheit - 273))
    except KeyError:
        temp_celsius_test = '999'
    if temp_celsius_test != '999':
        cur.execute("insert into cities (chat_id, city_name) "
                    "values (%s, %s)", (chat_id, city_name))
        conn_db.commit()
        what_to_send = city_name + ' горадок добавлен, ХУЯнДОК!'
    else:
        what_to_send = 'Нету такова хорада, брехун!'
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
                what_to_send = city_name + ' горадок удален, ХУЯнДОК!'
                bot.send_message(message.chat.id, what_to_send)
            except KeyError:
                pass
        else:
            bot.send_message(message.chat.id, 'Шо та пашло ни па плану!')
    except KeyError:
        bot.send_message(message.chat.id, 'Шо та пашло ни па плану!')


def add_temp_to_db(city_name, chat):
    temp = weather(city_name)
    cur.execute("update cities set temp=" + str(temp)
                + " where city_name='" + city_name
                + "' and chat_id='" + str(chat)
                + "'; ")
    conn_db.commit()


def weather_send(message, city_db, min_weather, max_weather, length):
    global what_to_send
    '''Checking max or min temp and send emoji near temp'''
    cur.execute("SELECT temp FROM cities where chat_id='"
                + str(message.chat.id) + "' and city_name='"
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


def get_weather_list(message):
    global what_to_send
    what_to_send = (
        'Вот вам ваша пагода па списачку, палучаица:\n')
    # getting cities list from DB
    cur.execute("SELECT city_name FROM cities "
                "where chat_id='" + str(message.chat.id) + "';")
    fetched_from_db = cur.fetchall()

    # updating temperatures in DB
    for i in range(0, len(fetched_from_db)):
        city_db = str(fetched_from_db[i]).replace("('", "").replace("',)", "")
        add_temp_to_db(city_db, message.chat.id)

    # find max and min weather in cities list
    if len(fetched_from_db) != 0:
        # max/min temp
        cur.execute("SELECT max(temp) FROM cities "
                    "where chat_id='" + str(message.chat.id) + "';")
        max_weather = int(
            str(cur.fetchall()).replace('[(', '').replace(',)]', ''))
        cur.execute("SELECT min(temp) FROM cities "
                    "where chat_id='" + str(message.chat.id) + "';")
        min_weather = int(
            str(cur.fetchall()).replace('[(', '').replace(',)]', ''))
        # parsing each city and temp from db
        for i in range(0, len(fetched_from_db)):
            city_db = str(
                fetched_from_db[i]).replace("('", "").replace("',)", "")
            weather_send(message,
                         city_db,
                         min_weather,
                         max_weather,
                         len(fetched_from_db))

        bot.send_message(
            chat_id=message.chat.id,
            text=what_to_send,
            parse_mode='Markdown')
    else:
        bot.send_message(
            chat_id=message.chat.id,
            text='Так нету харадов! Добавь командой /add <город>',
            parse_mode='Markdown')


# catching text message or command for bot
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    '''CATCHING COMMANDS'''
    # hru
    if message.text == '/хрю':
        hru = hru_list[random.randint(0, 21)]
        bot.send_sticker(message.chat.id, hru)
    # add city
    if message.text == '/add' or message.text == '/add@chupakabrada_bot':
        bot.send_message(message.chat.id, 'Пиши камандю так: /add город')
    elif message.text.split()[0] == '/add' or message.text.split()[0] == (
            '/add@chupakabrada_bot'):
        add_city(message)
    # delete city
    if message.text == '/delete' or message.text == '/delete@chupakabrada_bot':
        bot.send_message(message.chat.id, 'Пиши камандю так: /delete город')
    elif message.text.split()[0] == '/delete' or message.text.split()[0] == (
            '/delete@chupakabrada_bot'):
        delete_city(message)
    # weather on command
    if message.text == '/weather' or message.text == (
            '/weather@chupakabrada_bot'):
        bot.send_message(message.chat.id, 'Пиши камандю так: /weather город')
    elif message.text.split()[0] == '/weather' or message.text.split()[0] == (
            '/weather@chupakabrada_bot'):
        get_city_name(message)

    if message.text == '/weather_list' or message.text == (
            '/weather_list@chupakabrada_bot'):
        get_weather_list(message)

    # holiday on command
    if message.text == '/holiday' or message.text == (
            '/holiday@chupakabrada_bot'):
        os.system('python3 /root/telegram_chupakabrada_bot/holiday.py '
                  + str(message.chat.id))
    # coronavirus info on command
    if message.text == '/corona' or message.text == '/corona@chupakabrada_bot':
        os.system('python3 /root/telegram_chupakabrada_bot/today_corona.py '
                  + str(message.chat.id))
    # sticker pack on command
    if message.text == '/sticker' or message.text == (
            '/sticker@chupakabrada_bot'):
        query(51, message)
        for stick_id in range(1, 10):
            cur.execute("SELECT sticker FROM stickers "
                        "where sticker_id=" + str(stick_id) + " ")
            records = cur.fetchall()
            rec = (str(records[0]).replace("('", "")).replace("',)", "")
            bot.send_sticker(message.chat.id, rec)
            time.sleep(0.100)
    # start bot
    if message.text == '/start' or message.text == '/start@chupakabrada_bot':
        cur.execute("SELECT start_text FROM start_q where start_id=1")
        records = str(cur.fetchall()).replace("[('", "").replace("',)]", "")
        bot.send_message(message.chat.id, records)
    # about command
    if message.text == '/about' or message.text == '/about@chupakabrada_bot':
        cur.execute("SELECT about_text FROM about where about_id=1")
        records = str(cur.fetchall()).replace("[('", "").replace("',)]", "")
        bot.send_message(message.chat.id, records)
    # random quotes from db
    if message.text == '/quote' or message.text == '/quote@chupakabrada_bot':
        cur.execute("select quote from quotes where quote_id="
                    + str(random.randint(1, 180)) + " ")
        records = cur.fetchall()
        rec = (str(records[0]).replace("('", "")).replace("',)", "")
        bot.send_message(message.chat.id, rec)
    # random films from db
    if message.text == '/top_cinema' or message.text == (
            '/top_cinema@chupakabrada_bot'):
        cur.execute("select film from films where "
                    "film_id=" + str(random.randint(1, 250)) + " ")
        records = cur.fetchall()
        rec = (str(records[0]).replace("('", "")).replace("',)", "")
        bot.send_message(message.chat.id, rec)
    if message.text == '/random_cinema' or message.text == (
            '/random_cinema@chupakabrada_bot'):
        random_film = ('https://randomfilms.ru/film/'
                       + str(random.randint(1, 9600)))
        bot.send_message(message.chat.id, random_film)
    if message.text == key_for_stats:
        os.system('python3 /root/telegram_chupakabrada_bot/stats.py')

    # CATCHING MESSAGES
    # bot sends message if any word sent by user exists in DB
    check(message)

    # bot sends message if only one word sent by user
    # in chat and this word is in special dictionary
    msg = message.text.upper()
    cur.execute("SELECT msg_txt FROM messages")
    msg_db = str(cur.fetchall()).replace('[', '')\
        .replace("(\'", "").replace("\',),", " ")\
        .replace(",),", "").replace("',)]", "").split()
    if msg in msg_db:
        cur.execute("SELECT a.answer FROM answers a join messages m "
                    "on m.ans_id=a.ans_id where msg_txt='"
                    + msg + "' ")
        records = cur.fetchall()
        rec = (str(
            records[0]).replace("('", "")).replace("',)", "").replace(")", "")
        bot.send_message(message.chat.id, rec)

    # analytics
    st_chat_id = str(message.chat.id)
    st_name = (
        str(message.from_user.first_name)
        + " " + str(message.from_user.last_name)
    )
    st_nick = str(message.from_user.username)
    st_date = datetime.now()
    cur.execute("insert into stats (st_chat_id, st_name, st_nick, st_date) "
                "values (%s, %s, %s, %s)", (
                    st_chat_id, st_name, st_nick, st_date
                    )
                )
    conn_db.commit()


# catching audio files
@bot.message_handler(content_types=['voice'])
def get_voice_messages(voice):
    query(49, voice)


# catching audio files
@bot.message_handler(content_types=['audio'])
def get_audio_messages(audio):
    query(50, audio)


# auxiliary.py
'''
# for getting sticker id
@bot.message_handler(content_types=["sticker"])
def send_sticker(message):
    sticker_id = message.sticker.file_id
    bot.send_message(message.chat.id, sticker_id)


# for getting chat id
@bot.message_handler(content_types=["text"])
def chat_id(message):
    if message.text == 'chat':
        chat_id_var = message.chat.id
        bot.send_message(message.chat.id, chat_id_var)
'''


bot.polling(none_stop=True, interval=0, timeout=500)
