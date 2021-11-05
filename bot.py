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
from dictionary import *
import random
import pylightxl as xl
import logging
from bs4 import BeautifulSoup
from datetime import datetime

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
    what_to_send = 'Корона тайм зяблс. За сегодня в России: \n' \
                   'Заболевших ' + sick_change + ' \n' \
                   'Смертей ' + died_change + ' \n'
    return what_to_send


# checking does message has a word in list from dictionary
def check(message, diction, answer):
    msg_check = message.text.upper().split()
    dictionary = diction.upper().split()
    b = len(msg_check)
    i = 0
    while i < b:
        if msg_check[i] in dictionary:
            bot.send_message(message.chat.id, answer)
            i += 1
        else:
            i += 1


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
        bot.send_message(message.chat.id, answer_def_sticker)
        bot.send_sticker(message.chat.id, sticker_id1)
        bot.send_sticker(message.chat.id, sticker_id2)
        bot.send_sticker(message.chat.id, sticker_id3)
        bot.send_sticker(message.chat.id, sticker_id4)
        bot.send_sticker(message.chat.id, sticker_id5)
        bot.send_sticker(message.chat.id, sticker_id6)
        bot.send_sticker(message.chat.id, sticker_id7)
        bot.send_sticker(message.chat.id, sticker_id8)
        bot.send_sticker(message.chat.id, sticker_id9)
    # start bot
    if message.text == '/start' or message.text == '/start@chupakabrada_bot':
        bot.send_message(message.chat.id, answer_def_start)
    # random quotes from db
    if message.text == '/quote' or message.text == '/quote@chupakabrada_bot':
        db = xl.readxl(fn='quotes.xlsx', ws='Sheet1')
        rand = db.ws(ws='Sheet1').address(address='A' + str(random.randint(1, 180)))
        bot.send_message(message.chat.id, rand)
    # random films from db
    if message.text == '/top_cinema' or message.text == '/top_cinema@chupakabrada_bot':
        db = xl.readxl(fn='films.xlsx', ws='Sheet1')
        rand = db.ws(ws='Sheet1').address(address='E' + str(random.randint(1, 250)))
        bot.send_message(message.chat.id, rand)
    if message.text == '/random_cinema' or message.text == '/random_cinema@chupakabrada_bot':
        random_film = 'https://randomfilms.ru/film/' + str(random.randint(1, 9600))
        bot.send_message(message.chat.id, random_film)
    # catching messages
    # bot sends message if any word sent by user exists in dictionary
    check(message, hi, answer_hi)
    check(message, who_is_bot, answer_who_is_bot)
    check(message, abba, answer_abba)
    check(message, o, answer_o)
    check(message, full, answer_full)
    check(message, ass, answer_ass)
    check(message, note, answer_note)
    check(message, sorry, answer_sorry)
    check(message, birthday, answer_birthday)
    check(message, hello, answer_hello)
    check(message, dog, answer_dog)
    check(message, what, answer_what)
    check(message, smoke, answer_smoke)
    check(message, auto, answer_auto)
    check(message, grease, answer_grease)
    check(message, bull, answer_bull)
    check(message, u, answer_u)
    check(message, insta, answer_insta)
    check(message, penis, answer_penis)
    check(message, understand, answer_understand)
    check(message, cat, answer_cat)
    check(message, work, answer_work)
    check(message, serial, answer_serial)
    check(message, peace_death, answer_peace_death)
    check(message, steal, answer_steal)
    check(message, fool, answer_fool)
    check(message, sleep, answer_sleep)
    check(message, cake, answer_cake)
    check(message, how_are, answer_how_are)
    check(message, dream, answer_dream)
    check(message, old, answer_old)
    check(message, bad, answer_bad)
    check(message, good, answer_good)
    check(message, dish, answer_dish)
    check(message, soviet, answer_soviet)
    check(message, death, answer_death)
    random_check = random.randint(1, 100)
    if int(random_check/10) == 1 or int(random_check/10) == 2:
        check(message, god, answer_god)
    # bot sends message if only one word sent by user in chat
    msg = message.text.upper()
    if msg in message_lol:
        bot.send_message(message.chat.id, answer_message_lol)
    elif msg in message_plus:
        bot.send_message(message.chat.id, answer_message_plus)
    elif msg in message_aga:
        bot.send_message(message.chat.id, answer_message_aga)
    elif msg in message_steel:
        bot.send_message(message.chat.id, answer_message_steel)
    elif msg in message_wtf:
        bot.send_message(message.chat.id, answer_message_wtf)
    elif msg in message_sad:
        bot.send_message(message.chat.id, answer_message_sad)
    elif msg in message_a:
        bot.send_message(message.chat.id, answer_message_a)
    elif msg in message_no:
        bot.send_message(message.chat.id, answer_message_no)
    elif msg in message_thanks:
        bot.send_message(message.chat.id, answer_message_thanks)
    elif msg in message_who:
        bot.send_message(message.chat.id, answer_message_who)
        bot.send_sticker(message.chat.id, sticker_id1)
    # simple dialog with bot - first step
    elif message.text.upper() == bunny:
        bot.send_message(message.chat.id, what_bunny)
        bot.register_next_step_handler(message, get_bunny)


# simple dialog with bot - second step
def get_bunny(message):
    if message.text.upper() == yes:
        bot.send_message(message.chat.id, no_you_bunny)
    else:
        bot.send_message(message.chat.id, spit)


# catching audio files
@bot.message_handler(content_types=['voice'])
def get_voice_messages(voice):
    bot.send_message(voice.chat.id, answer_voice)


# catching audio files
@bot.message_handler(content_types=['audio'])
def get_audio_messages(audio):
    bot.send_message(audio.chat.id, answer_audio)


bot.polling(none_stop=True, interval=0, timeout=123)
