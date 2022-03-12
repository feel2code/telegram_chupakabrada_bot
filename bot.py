import logging

from connections import bot, cur
from conf import ban
from analytics import analytics
from constants import (
    COMMANDS_FUNCS, COMMANDS_DO, COMMANDS_QUERY, SELECTS, ZOO_DICT)
from selects import check, one_message, query, zoo


logging.basicConfig(
    level=logging.DEBUG,
    filename='main.log',
    format=(
        '%(asctime)s - %(module)s - %(levelname)s'
        ' - %(funcName)s: %(lineno)d - %(message)s'
    ),
    datefmt='%H:%M:%S',
)


# catching text messages or commands for bot
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    '''CATCHING COMMANDS'''
    deleting_msg(message)
    analytics(message)
    check(message)
    one_message(message)

    if message.text in SELECTS:
        standard_commands(message)

    if message.text in COMMANDS_FUNCS:
        COMMANDS_FUNCS[message.text](message.chat.id)

    if message.text in ZOO_DICT:
        zoo(message, ZOO_DICT[message.text])

    if message.text in COMMANDS_QUERY:
        query(COMMANDS_QUERY[message.text], message.chat.id)
    elif message.text.split()[0] in COMMANDS_DO:
        COMMANDS_DO[message.text.split()[0]](message)


def deleting_msg(message):
    """delete unappropriate words"""
    msg_check_ban: list = message.text.lower().split()
    for word in msg_check_ban:
        for msg_ban in ban:
            if msg_ban in word.lower():
                bot.delete_message(message.chat.id, message.id)


def standard_commands(message):
    cur.execute(SELECTS[message.text])
    records = cur.fetchone()[0]
    bot.send_message(message.chat.id, records)


@bot.message_handler(content_types=['voice'])
def get_voice_messages(voice):
    '''catching voice'''
    query(49, voice.chat.id)


@bot.message_handler(content_types=['audio'])
def get_audio_messages(audio):
    '''catching audio files'''
    query(50, audio.chat.id)


bot.polling(none_stop=True, interval=0, timeout=500)
