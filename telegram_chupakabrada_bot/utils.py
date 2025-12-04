import os

from telebot.apihelper import ApiTelegramException

from connections import SQLUtils, bot
from holiday import get_birthdays, get_holidays_from_db
from selects import rates_exchange
from weather_module import get_weather_list


def send_message(chat, message, parse_mode="Markdown"):
    """send sum message to the chat."""
    bot.send_message(chat_id=chat, text=message, parse_mode=parse_mode)


if __name__ == "__main__":
    db_conn = SQLUtils()
    chats_for_forecast_sending = db_conn.query(
        "select distinct chat_id from city_chat_id where scheduled_forecast=1;"
    )
    if isinstance(chats_for_forecast_sending, int):
        chats_for_forecast_sending = [chats_for_forecast_sending]
    for chat_id in chats_for_forecast_sending:
        try:
            weather = get_weather_list(chat_id)
            rates = rates_exchange(chat_id)
            holiday = get_holidays_from_db(chat_id)
            birthdays = get_birthdays()
            sum_message = (
                f"{weather}\n\n{rates}\n\nпраздники:\n{holiday}\n\n{birthdays}"
            )
            send_message(chat_id, sum_message)
        except ApiTelegramException as e:
            print(e)
