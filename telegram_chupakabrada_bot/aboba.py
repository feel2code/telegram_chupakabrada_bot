import os
from typing import Union

import markovify

from connections import SQLUtils, bot
from selects import query

markov_path = f"{'/'.join(os.getcwd().split('/')[:-1])}/markov_files/markov"


def markov(message) -> Union[str | None]:
    """processing message for Markov chains AI."""
    db_conn = SQLUtils()
    try:
        fetched = db_conn.query(
            f"select count(1) from markov where chat_id={message.chat.id}"
        )
    except IndexError:
        return None
    if fetched:
        hardness = db_conn.query(
            f"select hardness from markov where chat_id={message.chat.id};"
        )
        if hardness:
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
        print(path)
        if not os.path.exists(path):
            os.makedirs(path)
        with open(
            f"{markov_path}{str(message.chat.id)}.txt", "a", encoding="utf8"
        ) as markov_text:
            markov_text.write(f"{message.text}. ")
    return None


def markov_hardness_request(message):
    """checks correct modifying of hardness level."""
    if len(message.text.split(" ")) == 1:
        query(129, message.chat.id)
    else:
        markov_hardness(message)


def markov_hardness(message):
    """set hardness level of Markov chains AI."""
    # Искажения грамматики неслучайны.
    db_conn = SQLUtils()
    hardness = int(message.text.replace("/set ", "").replace(" ", "-"))
    count = db_conn.query(
        f"select count(1) from markov where chat_id={message.chat.id}"
    )
    hardness_list = list(range(1, 10))
    if count == 1:
        if hardness in hardness_list:
            db_conn.mutate(
                f"""update markov set hardness={hardness}
                    where chat_id={message.chat.id}"""
            )
            if hardness == hardness_list[-1]:
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
