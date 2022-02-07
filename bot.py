"""
This is funny bot for Telegram.
Bot can dialog with user in private or group chats, can reply for  often used words and phrases in chat,
can recommend stickers in chat by command.
Bot can send weather info by command and by CRON at definite time,
can send which holiday today in Russia by command and by CRON at definite time,
can send coronavirus actual info in Russia by command and by CRON at definite time.
Another JUST FOR FUN function - send one famous Russian YouTube streamer's quotes.
"""

import telebot
from conf import *
import random
import psycopg2
import os
from datetime import datetime
import time
import requests

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
            cur.execute(r"SELECT a.answer FROM questions as q join answers a on q.ans_id=a.ans_id where upper(q.question)='"
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
    rec = (str(records[0]).replace("('", "")).replace("',)", "").replace(")", "")
    bot.send_message(message.chat.id, rec)


def get_city_name(message):
    city = message.text.replace('/weather ', '').replace(' ', '-')
    try:
        req = requests.get('https://api.openweathermap.org/data/2.5/weather?q=' + city + '&appid=' + go_weather).json()
        city1 = req['main']
        city_temp = str(int(city1['temp'] - 273))
        cur.execute("SELECT answer FROM answers where ans_id=112")
        records = cur.fetchall()
        what_to_send = (str(records[0]).replace("('", "")).replace("',)", "").replace(")", "")
        what_to_send += ('\n ' + city_temp + ' °C ' + city)
    except:
        cur.execute("SELECT answer FROM answers where ans_id=111")
        records = cur.fetchall()
        what_to_send = (str(records[0]).replace("('", "")).replace("',)", "").replace(")", "")
    bot.send_message(message.chat.id, what_to_send)


# catching text message or command for bot
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    '''CATCHING COMMANDS'''
    # weather on command
    if message.text == '/weather' or message.text == '/weather@chupakabrada_bot':
        bot.send_message(message.chat.id, 'Пиши камандю так: /weather город')
    elif message.text.split()[0] == '/weather' or message.text.split()[0] == '/weather@chupakabrada_bot':
        bot.register_next_step_handler(message, get_city_name)



    # weather on command
    # if message.text == '/weather' or message.text == '/weather@chupakabrada_bot':
    #     bot.send_message(message.chat.id, 'А какой хород то?')
    #     bot.register_next_step_handler(message, city_name)
        # os.system('python3 /root/telegram_chupakabrada_bot/weather.py ' + str(message.chat.id))
    # holiday on command
    if message.text == '/holiday' or message.text == '/holiday@chupakabrada_bot':
        os.system('python3 /root/telegram_chupakabrada_bot/holiday.py ' + str(message.chat.id))
    # coronavirus info on command
    if message.text == '/corona' or message.text == '/corona@chupakabrada_bot':
        os.system('python3 /root/telegram_chupakabrada_bot/today_corona.py ' + str(message.chat.id))
    # sticker pack on command
    if message.text == '/sticker' or message.text == '/sticker@chupakabrada_bot':
        query(51, message)
        for stick_id in range(1, 10):
            cur.execute("SELECT sticker FROM stickers where sticker_id=" + str(stick_id) + " ")
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
        cur.execute("select quote from quotes where quote_id=" + str(random.randint(1, 180)) + " ")
        records = cur.fetchall()
        rec = (str(records[0]).replace("('", "")).replace("',)", "")
        bot.send_message(message.chat.id, rec)
    # random films from db
    if message.text == '/top_cinema' or message.text == '/top_cinema@chupakabrada_bot':
        cur.execute("select film from films where film_id=" + str(random.randint(1, 250)) + " ")
        records = cur.fetchall()
        rec = (str(records[0]).replace("('", "")).replace("',)", "")
        bot.send_message(message.chat.id, rec)
    if message.text == '/random_cinema' or message.text == '/random_cinema@chupakabrada_bot':
        random_film = 'https://randomfilms.ru/film/' + str(random.randint(1, 9600))
        bot.send_message(message.chat.id, random_film)
    if message.text == key_for_stats:
        os.system('python3 /root/telegram_chupakabrada_bot/stats.py')

    # CATCHING MESSAGES
    # bot sends message if any word sent by user exists in DB
    check(message)

    # bot sends message if only one word sent by user in chat and this word is in special dictionary
    msg = message.text.upper()
    cur.execute("SELECT msg_txt FROM messages")
    msg_db = str(cur.fetchall()).replace('[', '')\
        .replace("(\'", "").replace("\',),", " ")\
        .replace(",),", "").replace("',)]", "").split()
    if msg in msg_db:
        cur.execute("SELECT a.answer FROM answers a join messages m on m.ans_id=a.ans_id where msg_txt='"
                    + msg + "' ")
        records = cur.fetchall()
        rec = (str(records[0]).replace("('", "")).replace("',)", "").replace(")", "")
        bot.send_message(message.chat.id, rec)

    # analytics
    st_chat_id = str(message.chat.id)
    st_name = str(message.from_user.first_name) + " " + str(message.from_user.last_name)
    st_nick = str(message.from_user.username)
    st_date = datetime.now()
    cur.execute("insert into stats (st_chat_id, st_name, st_nick, st_date) "
                "values (%s, %s, %s, %s)", (st_chat_id, st_name, st_nick, st_date))
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

while True:
    try:
        bot.polling(none_stop=True, interval=0, timeout=500)
    except:
        pass
