import os

import markovify

from connections import bot, MySQLUtils
from selects import query

markov_path = f"{'/'.join(os.getcwd().split('/')[:-1])}/markov_files/markov"


def markov(message, db_conn: MySQLUtils):
    try:
        fetched = db_conn.query(f'select count(1) from markov where chat_id={message.chat.id}')[0]
    except IndexError:
        return
    if fetched:
        if fetched[0] == 1:
            hardness = db_conn.query(f'select hardness from markov where chat_id={message.chat.id};')[0]
            if hardness:
                hardness = hardness[0]
                markov_text = open(f'{markov_path}{str(message.chat.id)}.txt', 'a', encoding='utf-8')
                markov_text.write(f'{message.text}. ')
                markov_text.close()
                text = open(f'{markov_path}{str(message.chat.id)}.txt', encoding='utf8').read()
                try:
                    text_model = markovify.Text(text, state_size=int(hardness))
                except KeyError:
                    return
                for i in range(1):
                    return text_model.make_sentence(tries=50)
            else:
                return
        else:
            db_conn.mutate(f"insert into markov (chat_id, hardness) values ({message.chat.id}, 9);")
            markov_text = open(f'{markov_path}{str(message.chat.id)}.txt', "a")
            markov_text.write(f'{message.text}. ')
            markov_text.close()
            return message.text


def markov_hardness_request(message):
    db_conn = MySQLUtils()
    if len(message.text.split(' ')) == 1:
        query(129, message.chat.id, db_conn)
    else:
        markov_hardness(message)


def markov_hardness(message):
    """Искажения грамматики неслучайны."""
    db_conn = MySQLUtils()
    hardness = message.text.replace('/set ', '').replace(' ', '-')
    count = db_conn.query(f'select count(1) from markov where chat_id={message.chat.id}')[0][0]
    hardness_list = ('1', '2', '3', '4', '5', '6', '7', '8', '9')
    if count == 1:
        if hardness in hardness_list:
            hardness = int(hardness)
            db_conn.mutate(f'update markov set hardness={hardness} where chat_id={message.chat.id}')
            if hardness == int(hardness_list[-1]):
                msg_send = 'Заткнуть пытаешься да? Ну тада ясна.'
            else:
                msg_send = f'Мой ICQ уменьшился до {hardness}.'
            bot.send_message(message.chat.id, msg_send)
        else:
            bot.send_message(message.chat.id, f'Выбери из промежут_очка от {hardness_list[0]} до {hardness_list[-1]}')
    else:
        bot.send_message(message.chat.id, 'Поговори для начала са мною! Зззараза.')
