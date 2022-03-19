import markovify
from connections import cur, conn_db, bot


def markov(message):
    cur.execute(
        f'select count(1) from markov '
        f'where chat_id={message.chat.id}'
    )
    count = cur.fetchone()[0]
    if count == 1:
        sql = f'select hardness from markov where chat_id={message.chat.id};'
        cur.execute(sql)
        hardness = cur.fetchone()[0]
        markov_text = open(f'markov/markov{str(message.chat.id)}.txt', "a")
        markov_text.write(f'{message.text}. ')
        markov_text.close()
        text = open(
            f'markov/markov{str(message.chat.id)}.txt', encoding='utf8').read()
        text_model = markovify.Text(text)
        for i in range(1):
            return text_model.make_sentence(tries=hardness)
    else:
        cur.execute(
            f"insert into markov (chat_id, hardness) "
            f"values ({message.chat.id}, 50); "
        )
        conn_db.commit()
        markov_text = open(f'markov/markov{str(message.chat.id)}.txt', "a")
        markov_text.write(f'{message.text}. ')
        markov_text.close()
        return message.text


def markov_hardness(message):
    hardness = (
        message.text.replace('/set ', '').replace(' ', '-')
    )
    cur.execute(
        f'select count(1) from markov '
        f'where chat_id={message.chat.id}'
    )
    count = cur.fetchone()[0]
    if count == 1:
        if hardness in ('10', '50', '100'):
            hardness = int(hardness)
            cur.execute(
                f'update markov set hardness={hardness} '
                f'where chat_id={message.chat.id}'
            )
            conn_db.commit()
            bot.send_message(
                message.chat.id,
                f'Изменена болтливость на {hardness}'
            )
        else:
            bot.send_message(
                message.chat.id,
                'Выбери из: 10, 50, 100'
            )
    else:
        bot.send_message(
            message.chat.id,
            'Поговори для начала са мною!'
        )
