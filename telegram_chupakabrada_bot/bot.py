import logging
import os
import random

from telebot.apihelper import ApiTelegramException
from telebot.types import InputFile

from aboba import markov, markov_hardness_request
from analytics import analytics
from connections import bot
from films import films_command
from holiday import get_holidays_from_db, get_wiki_holiday
from selects import (
    check,
    get_about,
    get_quote,
    get_start,
    one_message,
    query,
    rates_exchange,
    roll,
    sticker_send,
    zoo,
)
from stats import send_statistics
from weather_module import (
    add_city_request,
    delete_city_request,
    get_weather_list,
    weather_in_city_request,
)

logging.basicConfig(
    level=logging.INFO,
    filename=f"{'/'.join(os.getcwd().split('/')[:-1])}/main.log",
    format=(
        "%(asctime)s - %(module)s - %(levelname)s - "
        "%(funcName)s: %(lineno)d - %(message)s"
    ),
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
logger.addHandler(handler)


def send_gs_voice(message):
    """sends voice message."""
    path = os.getenv("VOICES_PATH")
    bot.send_voice(
        message.chat.id, InputFile(f"{path}{random.choice(os.listdir(path))}")
    )


MAIN_CHAT_ID = int(os.getenv("HOME_TELEGA"))
COMMANDS_MAPPING = {
    "start": get_start,
    "about": get_about,
    "quote": get_quote,
    "forecast": get_weather_list,
    "holidays": get_holidays_from_db,
    "holiday": get_wiki_holiday,
    "sticker": sticker_send,
    "roll": roll,
    "usd": rates_exchange,
    "gel": rates_exchange,
    "add": add_city_request,
    "delete": delete_city_request,
    "weather": weather_in_city_request,
    "cinema": films_command,
    "set": markov_hardness_request,
    "хрю": zoo,
    "гав": zoo,
    "voice": send_gs_voice,
    os.getenv("KEY_FOR_STATS"): send_statistics,
}


@bot.message_handler(commands=list(COMMANDS_MAPPING.keys()))
def standard_commands_sender(message):
    """checks commands in message."""
    command = message.text.split()[0][1:].rstrip("@chupakabrada_bot")
    COMMANDS_MAPPING[command](message)


@bot.message_handler(content_types=["text"])
def get_text_messages(message):
    """Catching text messages or commands for bot."""
    if random.randint(1, 5) == 1:
        send_gs_voice(message)
    analytics(message)
    check(message)
    one_message(message)

    if "@all" in message.text and message.chat.id == MAIN_CHAT_ID:
        query(130, message.chat.id)

    ai_message = markov(message)
    if ai_message:
        bot.send_message(message.chat.id, ai_message)


def deleting_msg(message):
    """Delete unappropriated words."""
    # seek for space and other symbols
    for sym in (" ", "-", "_"):
        full_msg_ban = str(message.text.lower()).replace(sym, "")
    for msg_ban in os.getenv("BAN", None):
        if msg_ban in full_msg_ban:
            try:
                bot.delete_message(message.chat.id, message.id)
            except ApiTelegramException:
                logger.error("Issues with deleting unappropriated message.")


@bot.message_handler(content_types=["voice"])
def get_voice_messages(voice):
    """Catching voice messages for bot."""
    query(49, voice.chat.id)


@bot.message_handler(content_types=["audio"])
def get_audio_messages(audio):
    """Catching audio files."""
    query(50, audio.chat.id)


@bot.message_handler(content_types=["photo"])
def get_photo_messages(photo_message):
    """Catching messages sent with photos."""
    if photo_message.caption:
        if "@all" in photo_message.caption and photo_message.chat.id == MAIN_CHAT_ID:
            query(130, photo_message.chat.id)


if __name__ == "__main__":
    bot.polling(none_stop=True, interval=0, timeout=500)
