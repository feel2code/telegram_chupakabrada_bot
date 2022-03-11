import logging

from connections import bot, cur
from conf import key_for_stats, ban
from analytics import analytics
from constants import COMMANDS_QUERY, SELECTS, ZOO_DICT
from holiday import holiday
from selects import check, one_message, query, sticker_send
from films import films_command
from stats import send_statistics
from today_corona import coronavirus
from zoo import zoo
from weather_module import (
    weather_in_city, add_city, delete_city, get_weather_list)


logging.basicConfig(
    level=logging.DEBUG,
    filename='main.log',
    format=(
        '%(asctime)s - %(module)s - %(levelname)s'
        ' - %(funcName)s: %(lineno)d - %(message)s'
        ),
    datefmt='%H:%M:%S',
    )


COMMANDS_FUNCS = {
    key_for_stats: send_statistics,
    '/weather_list': get_weather_list,
    '/weather_list@chupakabrada_bot': get_weather_list,
    '/holiday': holiday,
    '/holiday@chupakabrada_bot': holiday,
    '/corona': coronavirus,
    '/corona@chupakabrada_bot': coronavirus,
    '/sticker': sticker_send,
    '/sticker@chupakabrada_bot': sticker_send,
}


# catching text messages or commands for bot
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    '''CATCHING COMMANDS'''
    analytics(message)
    check(message)
    one_message(message)

    if message.text in SELECTS:
        cur.execute(SELECTS[message.text])
        records = cur.fetchone()[0]
        bot.send_message(message.chat.id, records)

    if message.text in COMMANDS_FUNCS:
        COMMANDS_FUNCS[message.text](message.chat.id)

    if message.text in ZOO_DICT:
        zoo(message, ZOO_DICT[message.text])

    if message.text in COMMANDS_QUERY:
        query(COMMANDS_QUERY[message.text], message.chat.id)
    # add city
    elif message.text.split()[0] == '/add' or message.text.split()[0] == (
            '/add@chupakabrada_bot'):
        add_city(message)
    # delete city
    elif message.text.split()[0] == '/delete' or message.text.split()[0] == (
            '/delete@chupakabrada_bot'):
        delete_city(message)

    # top_cinema
    if message.text == '/top_cinema' or message.text == (
        '/top_cinema@chupakabrada_bot'
    ):
        films_command(message)

    # weather on command
    if message.text.split()[0] == '/weather' or message.text.split()[0] == (
            '/weather@chupakabrada_bot'):
        weather_in_city(message)

    # delete unappropriate words
    msg_check_ban: list = message.text.lower().split()
    for word in msg_check_ban:
        for msg_ban in ban:
            if msg_ban in word.lower():
                bot.delete_message(message.chat.id, message.id)


@bot.message_handler(content_types=['voice'])
def get_voice_messages(voice):
    '''catching voice'''
    query(49, voice.chat.id)


@bot.message_handler(content_types=['audio'])
def get_audio_messages(audio):
    '''catching audio files'''
    query(50, audio.chat.id)


bot.polling(none_stop=True, interval=0, timeout=500)
