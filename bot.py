import telebot
from conf import bot_token, db_name, weather_token, key_for_stats
import random
import psycopg2
import os
from datetime import datetime
import time
import requests

TEMPERATURE_NOT_EXIST = '999'
# connection to Bot
bot = telebot.TeleBot(bot_token)
# connection to DB
conn_db = psycopg2.connect(db_name)
cur = psycopg2.connect(db_name).cursor()


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
            rec = (cur.fetchone())[0]
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


def one_message(message):
    cur.execute('select count(1) from messages')
    msg_length = (cur.fetchall()[0])[0]
    cur.execute("SELECT msg_txt FROM messages")
    msg_db = cur.fetchall()
    msg_list = []
    for i in range(0, msg_length):
        msg_list.append((msg_db[i])[0])
    if message.text.upper() in msg_list:
        cur.execute(f"SELECT a.answer FROM answers a join messages m on "
                    f"m.ans_id=a.ans_id where "
                    f"msg_txt='{message.text.upper()}'")
        records = cur.fetchone()[0]
        bot.send_message(message.chat.id, records)


# query from db, get answer to send
def query(ans_id, message):
    cur.execute(f"SELECT answer FROM answers where ans_id={ans_id}")
    result = cur.fetchone()[0]
    bot.send_message(message.chat.id, result)


def simple_query(ans_id):
    cur.execute(f"SELECT answer FROM answers where ans_id={ans_id}")
    return cur.fetchone()[0]


def get_city_name(message):
    city = message.text.replace('/weather ', '').replace(' ', '-')
    try:
        req = requests.get(
            'https://api.openweathermap.org/data/2.5/weather?q=' + city
            + '&appid=' + weather_token).json()
        city1 = req['main']
        city_temp = str(int(city1['temp'] - 273))
        cur.execute("SELECT answer FROM answers where ans_id=112")
        what_to_send = (cur.fetchall()[0])[0]
        what_to_send += ('\n ' + city_temp + ' °C ' + city)
    except KeyError:
        cur.execute("SELECT answer FROM answers where ans_id=111")
        what_to_send = (cur.fetchall()[0])[0]
    bot.send_message(message.chat.id, what_to_send)


def weather(id: str) -> str:
    requestings = requests.get(
        f'https://api.openweathermap.org/data/2.5/'
        f'weather?q={id}&appid={weather_token}'
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
                what_to_send = city_name + ' ' + simple_query(121)
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


def weather_send(message, city_db, min_weather, max_weather, length):
    global what_to_send
    '''Checking max or min temp and send emoji near temp'''
    cur.execute("SELECT temp FROM cities where chat_id='"
                + str(message.chat.id) + "' and city_name='"
                + str(city_db) + "'; ")
    temp = int(cur.fetchone()[0])
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
    what_to_send = simple_query(122) + '\n'
    # getting cities list from DB
    cur.execute("SELECT city_name FROM cities "
                "where chat_id='" + str(message.chat.id) + "';")
    fetched_from_db = cur.fetchall()

    # updating temperatures in DB
    for i in range(0, len(fetched_from_db)):
        city_db = str((fetched_from_db[i])[0])
        add_temp_to_db(city_db, message.chat.id)

    # find max and min weather in cities list
    if len(fetched_from_db) != 0:
        # max/min temp
        cur.execute("SELECT max(temp) FROM cities "
                    "where chat_id='" + str(message.chat.id) + "';")
        max_weather = int((cur.fetchall()[0])[0])
        cur.execute("SELECT min(temp) FROM cities "
                    "where chat_id='" + str(message.chat.id) + "';")
        min_weather = int((cur.fetchall()[0])[0])
        # parsing each city and temp from db
        for i in range(0, len(fetched_from_db)):
            city_db = str((fetched_from_db[i])[0])
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
            text=simple_query(116),
            parse_mode='Markdown')


def get_top_films(message):
    try:
        year = int(message.text)
        if year in range(2017, 2023):
            cur.execute("select min(id), max(id) from films "
                        f"where year='{year}'")
            count_films = cur.fetchall()[0]
            random_id = str(random.randint(count_films[0], count_films[1] + 1))
            cur.execute("select film_name, year, link from films "
                        f"where id={random_id} and year='{year}'")
            records = ' '.join(cur.fetchall()[0])
            bot.send_message(message.chat.id, records)
        else:
            bot.send_message(message.chat.id, simple_query(117))
    except ValueError:
        bot.send_message(message.chat.id, simple_query(117))


def hru(message):
    random_id = str(random.randint(1, 23))
    cur.execute(f"SELECT sticker_id FROM pig_stickers where id={random_id}")
    sticker_id = (cur.fetchall()[0])[0]
    bot.send_sticker(message.chat.id, sticker_id)


# catching text message or command for bot
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    '''CATCHING COMMANDS'''
    # hru
    if message.text == '/хрю':
        hru(message)
    # add city
    if message.text == '/add' or message.text == '/add@chupakabrada_bot':
        bot.send_message(message.chat.id, simple_query(123))
    elif message.text.split()[0] == '/add' or message.text.split()[0] == (
            '/add@chupakabrada_bot'):
        add_city(message)
    # delete city
    if message.text == '/delete' or message.text == '/delete@chupakabrada_bot':
        bot.send_message(message.chat.id, simple_query(124))
    elif message.text.split()[0] == '/delete' or message.text.split()[0] == (
            '/delete@chupakabrada_bot'):
        delete_city(message)
    # weather on command
    if message.text == '/weather' or message.text == (
            '/weather@chupakabrada_bot'):
        bot.send_message(message.chat.id, simple_query(125))
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
            cur.execute(f"SELECT sticker FROM stickers "
                        f"where sticker_id={stick_id} ")
            records = cur.fetchone()[0]
            bot.send_sticker(message.chat.id, records)
            time.sleep(0.100)
    # start bot
    if message.text == '/start' or message.text == '/start@chupakabrada_bot':
        cur.execute("SELECT start_text FROM start_q where start_id=1")
        records = cur.fetchone()[0]
        bot.send_message(message.chat.id, records)
    # about command
    if message.text == '/about' or message.text == '/about@chupakabrada_bot':
        cur.execute("SELECT about_text FROM about where about_id=1")
        records = cur.fetchone()[0]
        bot.send_message(message.chat.id, records)
    # random quotes from db
    if message.text == '/quote' or message.text == '/quote@chupakabrada_bot':
        cur.execute("select quote from quotes where quote_id="
                    + str(random.randint(1, 180)) + " ")
        records = cur.fetchone()[0]
        bot.send_message(message.chat.id, records)
    # random films from db
    if message.text == '/top_cinema' or message.text == (
            '/top_cinema@chupakabrada_bot'):
        bot.send_message(
            message.chat.id,
            simple_query(118)
        )
        bot.register_next_step_handler(message, get_top_films)
    if message.text == key_for_stats:
        os.system('python3 /root/telegram_chupakabrada_bot/stats.py')

    # CATCHING MESSAGES
    # bot sends message if any word sent by user exists in DB
    check(message)

    # bot sends message if only one word sent by user
    # in chat and this word is in special dictionary
    one_message(message)

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
