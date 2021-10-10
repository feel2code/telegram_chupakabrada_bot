"""
This is funny bot for Telegram.
Bot can dialog with user in private or group chats, can reply for  often used words and phrases in chat.
Bot can send weather info by command and by CRON send weather info at definite time.
Another JUST FOR FUN function - send quotes from known in Russia YouTube streamer.
"""

import telebot
import requests
from conf import *
from dictionary import *
import random
import pylightxl as xl

# global variables
bot = telebot.TeleBot(name)
k4 = ''
p4 = ''
m4 = ''
e4 = ''


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
    global m4
    r = requests.get('http://api.openweathermap.org/data/2.5/weather?q=moscow&appid='+go_weather)
    m = r.json()
    m1 = m['main']
    m2 = m1['temp']
    m3 = int(m2 - 273)
    m4 = str(m3)
    return m4


def weather_ekb():
    global e4
    r = requests.get('http://api.openweathermap.org/data/2.5/weather?id=1486209&appid='+go_weather)
    e = r.json()
    e1 = e['main']
    e2 = e1['temp']
    e3 = int(e2 - 273)
    e4 = str(e3)
    return e4


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
    global m4
    global e4
    # weather on command
    if message.text == '/weather' or message.text == '/weather@chupakabrada_bot':
        weather_kzn()
        weather_spb()
        weather_msk()
        weather_ekb()
        what_to_send = ('Пагода в районах-харадах \n '+k4+' °C Казань \n ' + p4)
        what_to_send += (' °C Питер \n ' + m4 + ' °C Москва \n ' + e4 + ' °C Екб \n ')
        bot.send_message(message.chat.id, what_to_send)
    # sticker pack on command
    if message.text == '/sticker':
        bot.send_message(message.chat.id, answer_def_sticker)
    # start bot
    if message.text == '/start':
        bot.send_message(message.chat.id, answer_def_start)
    # random quotes from db
    if message.text == '/quote' or message.text == '/quote@chupakabrada_bot':
        db = xl.readxl(fn='quotes.xlsx', ws='Sheet1')
        rand = db.ws(ws='Sheet1').address(address='A' + str(random.randint(1, 180)))
        bot.send_message(message.chat.id, rand)
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


bot.polling(none_stop=True, interval=0)
