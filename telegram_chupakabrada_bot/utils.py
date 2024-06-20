import os

from connections import bot
from holiday import get_holidays_from_db
from selects import rates_exchange
from weather_module import get_weather_list


def send_message(chat, message, parse_mode="Markdown"):
    """send sum message to the chat."""
    bot.send_message(chat_id=chat, text=message, parse_mode=parse_mode)


if __name__ == "__main__":
    chat_id = os.getenv("HOME_TELEGA")
    weather = get_weather_list(chat_id)
    rates = rates_exchange(chat_id)
    holiday = get_holidays_from_db(chat_id)
    sum_message = f"{weather}\n\n{rates}\n\nПраздники:\n{holiday}"
    send_message(chat_id, sum_message)
