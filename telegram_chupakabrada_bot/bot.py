import logging

from analysis.analytics import analytics
from analysis.stats import send_statistics
from conf import ban, home_telega, key_for_stats
from connections import bot, cur
from constants import COMMANDS_QUERY, SELECTS, ZOO_DICT
from features.films import films_command
from features.holiday import holiday
from features.weather_module import add_city, delete_city, get_weather_list, weather_in_city
from markov.aboba import markov, markov_hardness
from selects import check, exchange, one_message, query, roll, sticker_send, zoo
from today_corona import coronavirus
from telebot.apihelper import ApiTelegramException


logging.basicConfig(
    level=logging.DEBUG,
    filename='main.log',
    format=(
        '%(asctime)s - %(module)s - %(levelname)s'
        ' - %(funcName)s: %(lineno)d - %(message)s'
    ),
    datefmt='%H:%M:%S',
)
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
logger.addHandler(handler)

COMMANDS_DO = {
    '/add': add_city,
    '/add@chupakabrada_bot': add_city,
    '/delete': delete_city,
    '/delete@chupakabrada_bot': delete_city,
    '/weather': weather_in_city,
    '/weather@chupakabrada_bot': weather_in_city,
    '/top_cinema': films_command,
    '/top_cinema@chupakabrada_bot': films_command,
    '/set': markov_hardness,
    '/set@chupakabrada_bot': markov_hardness
}

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
    '/roll': roll,
    '/roll@chupakabrada_bot': roll,
    '/dollar': exchange,
    '/dollar@chupakabrada_bot': exchange
}


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    """Catching text messages or commands for bot."""
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

    if '@all' in message.text and message.chat.id == int(home_telega):
        query(130, home_telega)

    ai_message = markov(message)
    if ai_message is not None:
        bot.send_message(message.chat.id, ai_message)


def deleting_msg(message):
    """Delete unappropriated words."""
    # seek for space and other symbols
    for sym in (' ', '-', '_'):
        full_msg_ban = str(message.text.lower()).replace(sym, '')
    for msg_ban in ban:
        if msg_ban in full_msg_ban:
            try:
                bot.delete_message(message.chat.id, message.id)
            except ApiTelegramException:
                logger.error('Issues with deleting unappropriated message.')


def standard_commands(message):
    """Do something by commands in SELECTS constants."""
    cur.execute(SELECTS[message.text])
    bot.send_message(message.chat.id, cur.fetchone()[0])


@bot.message_handler(content_types=['voice'])
def get_voice_messages(voice):
    """Catching voice messages for bot."""
    query(49, voice.chat.id)


@bot.message_handler(content_types=['audio'])
def get_audio_messages(audio):
    """Catching audio files."""
    query(50, audio.chat.id)


@bot.message_handler(content_types=['photo'])
def get_photo_messages(photo_message):
    """Catching messages sent with photos."""
    if photo_message.caption is not None:
        if '@all' in photo_message.caption and photo_message.chat.id == int(home_telega):
            query(130, home_telega)


bot.polling(none_stop=True, interval=0, timeout=500)
