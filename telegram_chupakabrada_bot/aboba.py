import os
from typing import Union

import markovify

from connections import SQLUtils, bot
from selects import query

markov_path = f"{'/'.join(os.getcwd().split('/')[:-1])}/markov_files/markov"


def markov(message, db_conn: SQLUtils) -> Union[str | None]:
    """processing message for Markov chains AI."""
    try:
        fetched = db_conn.query(
            f"select count(1) from markov where chat_id={message.chat.id}"
        )[0]
    except IndexError:
        return None
    if fetched:
        if fetched[0] == 1:
            hardness = db_conn.query(
                f"select hardness from markov where chat_id={message.chat.id};"
            )[0]
            if hardness:
                hardness = hardness[0]

                with open(
                    f"{markov_path}{str(message.chat.id)}.txt", "a", encoding="utf-8"
                ) as markov_text:
                    markov_text.write(f"{message.text}. ")

                with open(
                    f"{markov_path}{str(message.chat.id)}.txt", encoding="utf8"
                ) as text:
                    try:
                        text_model = markovify.Text(text, state_size=int(hardness))
                        return text_model.make_sentence(tries=50)
                    except KeyError:
                        return None
            else:
                return None
        else:
            db_conn.mutate(
                f"""insert into markov (chat_id, hardness)
                    values ({message.chat.id}, 9);"""
            )
            path = f"{'/'.join(os.getcwd().split('/')[:-1])}/markov_files"
            if not os.path.exists(path):
                os.makedirs(path)
            with open(
                f"{markov_path}{str(message.chat.id)}.txt", "a", encoding="utf8"
            ) as markov_text:
                markov_text.write(f"{message.text}. ")
    return None


def markov_hardness_request(message):
    """checks correct modifying of hardness level."""
    db_conn = SQLUtils()
    if len(message.text.split(" ")) == 1:
        query(129, message.chat.id, db_conn)
    else:
        markov_hardness(message)


def markov_hardness(message):
    """set hardness level of Markov chains AI."""
    # Искажения грамматики неслучайны.
    db_conn = SQLUtils()
    hardness = message.text.replace("/set ", "").replace(" ", "-")
    count = db_conn.query(
        f"select count(1) from markov where chat_id={message.chat.id}"
    )[0][0]
    hardness_list = ("1", "2", "3", "4", "5", "6", "7", "8", "9")
    if count == 1:
        if hardness in hardness_list:
            hardness = int(hardness)
            db_conn.mutate(
                f"""update markov set hardness={hardness}
                    where chat_id={message.chat.id}"""
            )
            if hardness == int(hardness_list[-1]):
                msg_send = "Заткнуть пытаешься да? Ну тада ясна."
            else:
                msg_send = f"Мой ICQ уменьшился до {hardness}."
            bot.send_message(message.chat.id, msg_send)
        else:
            bot.send_message(
                message.chat.id,
                (
                    f"Выбери из промежут_очка от {hardness_list[0]}"
                    f"до {hardness_list[-1]}"
                ),
            )
    else:
        bot.send_message(message.chat.id, "Поговори для начала са мною! Зззараза.")
