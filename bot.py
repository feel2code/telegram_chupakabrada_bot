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
import requests
from conf import *
import random
import logging
from bs4 import BeautifulSoup
from datetime import datetime
import psycopg2

conn_db = psycopg2.connect(conn)
# connect to db
cur = conn_db.cursor()

# global variables
bot = telebot.TeleBot(name)
k4 = ''
p4 = ''
msc4 = ''
e4 = ''
what_to_send = ''
data = ''
m1 = 'января'
m2 = 'февраля'
m3 = 'марта'
m4 = 'апреля'
m5 = 'мая'
m6 = 'июня'
m7 = 'июля'
m8 = 'августа'
m9 = 'сентября'
m10 = 'октября'
m11 = 'ноября'
m12 = 'декабря'
day = datetime.now().day
month = datetime.now().month
message_lol = ['ХЕХ', 'АХАХАХ', 'АХАХАХАХ', 'ЛОЛ', 'ХАХА']
message_plus = ['+', '++', '+++', '++++']
message_aga = ['АГА']
message_steel = ['ЖЕСТЬ']
message_wtf = [')', '))', ')))', '))))', ')))))']
message_sad = ['(', '((', '(((', '((((', '(((((']
message_a = ['А', 'АА', 'ААА', 'АААА']
message_who = ['ХТО', 'КТО', 'КТО?', 'ХТО?']
message_no = ['НЕ', 'НЕТ', 'НЕА', 'НЕТ(', 'НЕТ)']
message_thanks = ['СПС', 'SPS']
answer_def_start = 'Да шо тут гаварити, могу болтать с вами в группе или в чатике.' \
                   ' Добавляй в чат, даб даб даб, зяблс. Могу погоду гаварить. ' \
                   'Магу стикеры пасаветавать или фильмы, ну дя. \n ' \
                   'Разработка и поддержка - @stealingyou \n' \
                   'Данатики Юmoney - 4100117291947258'
# logging bot
log = telebot.logger
logging.basicConfig(filename='chupakabra.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)


def weather_kzn():
    global k4
    r = requests.get('http://api.openweathermap.org/data/2.5/weather?q=kazan&appid='+go_weather)
    k = r.json()
    k1 = k['main']
    k2 = k1['temp']
    k3 = int(k2 - 273)
    k4 = str(k3)
    return k4


def weather_spb():
    global p4
    r = requests.get('http://api.openweathermap.org/data/2.5/weather?id=498817&appid='+go_weather)
    p = r.json()
    p1 = p['main']
    p2 = p1['temp']
    p3 = int(p2 - 273)
    p4 = str(p3)
    return p4


def weather_msk():
    global msc4
    r = requests.get('http://api.openweathermap.org/data/2.5/weather?q=moscow&appid='+go_weather)
    m = r.json()
    msc1 = m['main']
    msc2 = msc1['temp']
    msc3 = int(msc2 - 273)
    msc4 = str(msc3)
    return msc4


def weather_ekb():
    global e4
    r = requests.get('http://api.openweathermap.org/data/2.5/weather?id=1486209&appid='+go_weather)
    e = r.json()
    e1 = e['main']
    e2 = e1['temp']
    e3 = int(e2 - 273)
    e4 = str(e3)
    return e4


def corona():
    global what_to_send
    page = requests.get('https://стопкоронавирус.рф/information/')
    soup = BeautifulSoup(page.text, "html.parser")
    found = soup.select('cv-stats-virus')
    found = str(found).split(':stats-data=')
    found = str(found[1]).split(',')
    sick_change = str(found[1]).replace('"sickChange":"', '')
    sick_change = sick_change.replace('"', '')
    died_change = str(found[5]).replace('"diedChange":"', '')
    died_change = died_change.replace('"', '')
    died_change = died_change.replace(r'\u00a0', ' ')
    what_to_send = 'Корона тайм зяблс. За сегодня в России: \n' \
                   'Заболевших ' + sick_change + ' \n' \
                   'Смертей ' + died_change + ' \n'
    return what_to_send


# checking does message has a word in list from dictionary
def check(message):
    msg_check = message.text.upper().split()
    b = len(msg_check)
    i = 0
    while i < b:
        quest = msg_check[i]
        cur.execute(r"SELECT a.answer FROM questions as q join answers a "
                    r"on q.ans_id=a.ans_id where upper(q.question)='" + quest + "' ")
        # Retrieve query results
        records = cur.fetchall()
        try:
            rec = (str(records[0]).replace("('", ""))
            rec = rec.replace("',)", "")
            bot.send_message(message.chat.id, rec)
            i += 1
        except:
            i += 1


# query from db, get answer to send
def query(ans_id, message):
    cur.execute("SELECT answer FROM answers where ans_id=" + str(ans_id) + " ")
    records = cur.fetchall()
    rec = (str(records[0]).replace("('", ""))
    rec = rec.replace("',)", "")
    bot.send_message(message.chat.id, rec)


def stick(stick_id, message):
    cur.execute("SELECT sticker FROM stickers where sticker_id=" + str(stick_id) + " ")
    records = cur.fetchall()
    rec = (str(records[0]).replace("('", ""))
    rec = rec.replace("',)", "")
    bot.send_sticker(message.chat.id, rec)


# catching text message or command for bot
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    # catching command
    global k4
    global p4
    global msc4
    global e4
    global what_to_send
    global data
    # weather on command
    if message.text == '/weather' or message.text == '/weather@chupakabrada_bot':
        weather_kzn()
        weather_spb()
        weather_msk()
        weather_ekb()
        what_to_send = ('Пагода в районах-харадах \n '+k4+' °C Казань \n ' + p4)
        what_to_send += (' °C Питер \n ' + msc4 + ' °C Москва \n ' + e4 + ' °C Екб \n ')
        bot.send_message(message.chat.id, what_to_send)
    # holiday on command
    if message.text == '/holiday' or message.text == '/holiday@chupakabrada_bot':
        today = []
        if month == 1:
            data = str(day) + '_' + m1
        elif month == 2:
            data = str(day) + '_' + m2
        elif month == 3:
            data = str(day) + '_' + m3
        elif month == 4:
            data = str(day) + '_' + m4
        elif month == 5:
            data = str(day) + '_' + m5
        elif month == 6:
            data = str(day) + '_' + m6
        elif month == 7:
            data = str(day) + '_' + m7
        elif month == 8:
            data = str(day) + '_' + m8
        elif month == 9:
            data = str(day) + '_' + m9
        elif month == 10:
            data = str(day) + '_' + m10
        elif month == 11:
            data = str(day) + '_' + m11
        elif month == 12:
            data = str(day) + '_' + m12
        page = requests.get('https://ru.wikipedia.org/wiki/' + 'Категория:Праздники_' + data)
        soup = BeautifulSoup(page.text, "html.parser")
        for item in soup.select("li"):
            today.append(item.get_text())
        index = today.index('Праздники' + data.replace(str(day) + '_', ' '))
        i = index
        while len(today) != i:
            today.pop(index)
        today[0] = ' ' + today[0]
        case = str([word + '\n' for word in today])
        case1 = case.replace(',', '')
        case2 = case1.replace('[', '')
        case3 = case2.replace(']', '')
        case4 = case3.replace('[', '')
        case5 = case4.replace("'", "")
        case6 = case5.replace(r"\n", "\n")
        bot.send_message(message.chat.id, text=('Сиводня палучаица ' + str(datetime.now().date()) + ': \n' + case6))
    # coronavirus info on command
    if message.text == '/corona' or message.text == '/corona@chupakabrada_bot':
        corona()
        bot.send_message(message.chat.id, text=what_to_send)
    # sticker pack on command
    if message.text == '/sticker' or message.text == '/sticker@chupakabrada_bot':
        query(51, message)
        for i in range(1, 10):
            stick(i, message)
    # start bot
    if message.text == '/start' or message.text == '/start@chupakabrada_bot':
        bot.send_message(message.chat.id, answer_def_start)
    # random quotes from db
    if message.text == '/quote' or message.text == '/quote@chupakabrada_bot':
        cur.execute("select quote from quotes where quote_id=" + str(random.randint(1, 180)) + " ")
        records = cur.fetchall()
        rec = (str(records[0]).replace("('", ""))
        rec = rec.replace("',)", "")
        bot.send_message(message.chat.id, rec)
    # random films from db
    if message.text == '/top_cinema' or message.text == '/top_cinema@chupakabrada_bot':
        cur.execute("select film from films where film_id=" + str(random.randint(1, 250)) + " ")
        records = cur.fetchall()
        rec = (str(records[0]).replace("('", ""))
        rec = rec.replace("',)", "")
        bot.send_message(message.chat.id, rec)
    if message.text == '/random_cinema' or message.text == '/random_cinema@chupakabrada_bot':
        random_film = 'https://randomfilms.ru/film/' + str(random.randint(1, 9600))
        bot.send_message(message.chat.id, random_film)
    # catching messages
    # bot sends message if any word sent by user exists in DB
    check(message)
    # bot sends message if only one word sent by user in chat
    msg = message.text.upper()
    if msg in message_lol:
        query(39, message)
    elif msg in message_plus:
        query(40, message)
    elif msg in message_aga:
        query(41, message)
    elif msg in message_steel:
        query(42, message)
    elif msg in message_wtf:
        query(43, message)
    elif msg in message_sad:
        query(44, message)
    elif msg in message_a:
        query(45, message)
    elif msg in message_no:
        query(46, message)
    elif msg in message_thanks:
        query(47, message)
    elif msg in message_who:
        query(48, message)


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

bot.polling(none_stop=True, interval=0, timeout=123)
