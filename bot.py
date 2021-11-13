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

conn_db = psycopg2.connect(conn)
# connect to db
cur = conn_db.cursor()

# global variables
bot = telebot.TeleBot(name)
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
                   'Данатики Юмани - 4100117291947258'


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
        except IndexError:
            i += 1


# query from db, get answer to send
def query(ans_id, message):
    cur.execute("SELECT answer FROM answers where ans_id=" + str(ans_id) + " ")
    records = cur.fetchall()
    rec = (str(records[0]).replace("('", ""))
    rec = rec.replace("',)", "")
    rec = rec.replace(")", "")
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
    # weather on command
    if message.text == '/weather' or message.text == '/weather@chupakabrada_bot':
        os.system('python3 /root/telegram_chupakabrada_bot/weather.py ' + str(message.chat.id))
    # holiday on command
    if message.text == '/holiday' or message.text == '/holiday@chupakabrada_bot':
        os.system('python3 /root/telegram_chupakabrada_bot/holiday.py ' + str(message.chat.id))
    # coronavirus info on command
    if message.text == '/corona' or message.text == '/corona@chupakabrada_bot':
        os.system('python3 /root/telegram_chupakabrada_bot/today_corona.py ' + str(message.chat.id))
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
