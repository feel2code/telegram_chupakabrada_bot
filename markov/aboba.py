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
        text_model = markovify.Text(text, state_size=int(hardness))
        for i in range(1):
            return text_model.make_sentence(tries=50)
    else:
        cur.execute(
            f"insert into markov (chat_id, hardness) "
            f"values ({message.chat.id}, 1); "
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
    hardness_list = ('1', '2', '3', '4', '5', '6', '7', '8', '9')
    if count == 1:
        if hardness in hardness_list:
            hardness = int(hardness)
            cur.execute(
                f'update markov set hardness={hardness} '
                f'where chat_id={message.chat.id}'
            )
            conn_db.commit()
            bot.send_message(
                message.chat.id,
                f'Умственные способности теперь на уровне {hardness}'
            )
        else:
            bot.send_message(
                message.chat.id,
                f'Выбери из: {str(hardness_list)}'
            )
    else:
        bot.send_message(
            message.chat.id,
            'Поговори для начала са мною!'
        )
