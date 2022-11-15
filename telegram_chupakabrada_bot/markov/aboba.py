import markovify

from connections import bot, conn_db, cur


def markov(message):
    cur.execute(f'select count(1) from markov where chat_id={message.chat.id}')
    if cur.fetchone()[0] == 1:
        cur.execute(f'select hardness from markov where chat_id={message.chat.id};')
        hardness = cur.fetchone()[0]
        markov_text = open(f'markov/markov{str(message.chat.id)}.txt', "a")
        markov_text.write(f'{message.text}. ')
        markov_text.close()
        text = open(f'markov/markov{str(message.chat.id)}.txt', encoding='utf8').read()
        text_model = markovify.Text(text, state_size=int(hardness))
        for i in range(1):
            return text_model.make_sentence(tries=50)
    else:
        cur.execute(f"insert into markov (chat_id, hardness) values ({message.chat.id}, 1);")
        conn_db.commit()
        markov_text = open(f'markov/markov{str(message.chat.id)}.txt', "a")
        markov_text.write(f'{message.text}. ')
        markov_text.close()
        return message.text


def markov_hardness(message):
    """Искажения грамматики неслучайны."""
    hardness = message.text.replace('/set ', '').replace(' ', '-')
    cur.execute(f'select count(1) from markov where chat_id={message.chat.id}')
    count = cur.fetchone()[0]
    hardness_list = ('1', '2', '3', '4', '5', '6', '7', '8', '9')
    if count == 1:
        if hardness in hardness_list:
            hardness = int(hardness)
            cur.execute(f'update markov set hardness={hardness} where chat_id={message.chat.id}')
            conn_db.commit()
            if hardness == int(hardness_list[0]):
                msg_send = f'Мой ICQ уменьшился до {hardness}.'
            else:
                msg_send = 'Заткнуть пытаешься да? Ну тада ясна.'
            bot.send_message(message.chat.id, msg_send)
        else:
            bot.send_message(message.chat.id, f'Выбери из промежут_очка от {hardness_list[0]} до {hardness_list[-1]}')
    else:
        bot.send_message(message.chat.id, 'Поговори для начала са мною! Зззараза.')
