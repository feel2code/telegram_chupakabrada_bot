from telegram_chupakabrada_bot.connections import bot, cur
from telegram_chupakabrada_bot.selects import query, simple_query


def films_command(message):
    query(118, message.chat.id)
    bot.register_next_step_handler(message, get_top_films)


def get_top_films(message):
    try:
        year = int(message.text)
        if year in range(2017, 2023):
            cur.execute(f"select film_name, year, link from films where year='{year}' order by random() limit 1")
            what_to_send = ' '.join(cur.fetchall()[0])
        else:
            what_to_send = simple_query(117)
    except IndexError:
        what_to_send = simple_query(117)
    except ValueError:
        what_to_send = simple_query(117)
    bot.send_message(message.chat.id, what_to_send)
