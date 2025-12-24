from telebot.util import quick_markup

from connections import SQLUtils, bot
from selects import query, simple_query


def films_command(message):
    bot.send_message(message.chat_id, "Какого хода нужен фильм? А ню давай!")
    db_conn = SQLUtils()
    bot.register_next_step_handler(message, get_top_films, db_conn)


def send_film(chat_id, year):
    db_conn = SQLUtils()
    film = " ".join(
        db_conn.query(
            f"""select film_name, film_year, link
                    from films
                    where film_year='{year}' order by random() limit 1"""
        )
    )
    bot.send_message(chat_id, film)
    bot.send_message(chat_id, "Еще?", reply_markup=get_inline_keys(year))


def get_inline_keys(year):
    return quick_markup(
        {"ДА": {"callback_data": f"{year}"}, "НЕТ": {"callback_data": "no"}},
        row_width=2,
    )


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "no":
        bot.send_message(call.message.chat.id, simple_query(46))
        return
    send_film(call.message.chat.id, call.data)


def get_top_films(message, db_conn: SQLUtils):
    try:
        year = int(message.text)
        min_year, max_year = db_conn.query(
            """select min(cast(film_year as UNSIGNED)),
                      max(cast(film_year as UNSIGNED)) from films;"""
        )
        if year in range(min_year, max_year + 1):
            send_film(message.chat.id, year)
            return
        what_to_send = simple_query(117)
    except IndexError:
        what_to_send = simple_query(117)
    except ValueError:
        what_to_send = simple_query(117)
    bot.send_message(message.chat.id, what_to_send)
