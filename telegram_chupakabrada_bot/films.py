from connections import bot, MySQLUtils
from selects import query, simple_query


def films_command(message):
    db_conn = MySQLUtils()
    query(118, message.chat.id, db_conn)
    bot.register_next_step_handler(message, get_top_films, db_conn)


def get_top_films(message, db_conn: MySQLUtils):
    try:
        year = int(message.text)
        min_year, max_year = db_conn.query(
            f"select min(cast(film_year as UNSIGNED)), max(cast(film_year as UNSIGNED)) from films;"
        )[0]
        if year in range(min_year, max_year + 1):
            what_to_send = ' '.join(db_conn.query(
                f"select film_name, film_year, link from films where film_year='{year}' order by rand() limit 1"
            )[0])
        else:
            what_to_send = simple_query(117)
    except IndexError:
        what_to_send = simple_query(117)
    except ValueError:
        what_to_send = simple_query(117)
    bot.send_message(message.chat.id, what_to_send)
