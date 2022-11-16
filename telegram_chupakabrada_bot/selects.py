import time
from datetime import datetime

import psycopg2

from telegram_chupakabrada_bot.connections import bot, conn_db, cur
from telegram_chupakabrada_bot.constants import GODZILLA


# checking does message has any word in list from dictionary
def check(message):
    msg_check = message.text.upper().split()
    for word in msg_check:
        cur.execute(f"""select a.answer from questions as q join answers a on q.ans_id=a.ans_id
                        where upper(q.question)='{word}';""")
        try:
            rec = cur.fetchone()
        except psycopg2.ProgrammingError:
            continue
        if not rec:
            continue
        else:
            rec = rec[0]
        if rec == GODZILLA:
            query(103, message.chat.id)
            time.sleep(1)
            i_count = 104
            while i_count < 111:
                query(i_count, message.chat.id)
                time.sleep(0.100)
                i_count += 1
            i_count = 109
            while i_count > 103:
                query(i_count, message.chat.id)
                time.sleep(0.100)
                i_count = i_count - 1
            continue
        else:
            bot.send_message(message.chat.id, rec)


def one_message(message):
    cur.execute('select count(1) from messages')
    try:
        msg_length = cur.fetchone()
        if msg_length:
            msg_length = msg_length[0]
        else:
            return
    except psycopg2.ProgrammingError:
        return
    cur.execute("select msg_txt from messages")
    msg_db = cur.fetchall()
    msg_list = []
    for i in range(0, msg_length):
        msg_list.append((msg_db[i])[0])
    if message.text.upper() in msg_list:
        cur.execute(f"""select a.answer from answers a join messages m on m.ans_id=a.ans_id
                        where msg_txt='{message.text.upper()}';""")
        records = cur.fetchone()[0]
        bot.send_message(message.chat.id, records)


def simple_query(ans_id):
    """query from answers table."""
    cur.execute(f"select answer from answers where ans_id={ans_id};")
    return cur.fetchone()[0]


def query(ans_id, chat_id):
    """send message to chat."""
    bot.send_message(chat_id=chat_id, text=simple_query(ans_id))


def sticker_send(chat_id):
    """send stickers to chat."""
    query(51, chat_id)
    for stick_id in range(1, 10):
        cur.execute(f"select sticker from stickers where sticker_id={stick_id};")
        records = cur.fetchone()[0]
        bot.send_sticker(chat_id=chat_id, data=records)
        time.sleep(0.200)


def zoo(message, sticker_family):
    """send sticker via animal-like-codeword to chat."""
    cur.execute(f"select sticker_id from {sticker_family} order by random() limit 1;")
    sticker_id = cur.fetchone()[0]
    bot.send_sticker(message.chat.id, sticker_id)


def roll(chat_id: int):
    """roll someone in chat."""
    cur.execute(
        f"select count(1) from rolls where chat_id='{chat_id}' and date='{datetime.today().strftime('%Y-%m-%d')}';"
    )
    count = cur.fetchone()[0]
    if count == 0:
        cur.execute(f"""select * from (select distinct st_nick from stats
                                       where st_chat_id='{chat_id}' and st_nick != 'None') as foo
                        order by random() limit 1;""")
        nick = cur.fetchone()[0]
        bot.send_message(chat_id=chat_id, text=f'Великий рандом выбрал тебя, @{nick}')
        cur.execute(f"insert into rolls values('{nick}', '{chat_id}', '{datetime.today().strftime('%Y-%m-%d')}');")
        conn_db.commit()
    else:
        cur.execute(
            f"select nick from rolls where chat_id='{chat_id}' and date='{datetime.today().strftime('%Y-%m-%d')}';"
        )
        nick = cur.fetchone()[0]
        bot.send_message(chat_id=chat_id, text=f'Великий рандом выбрал тебя, @{nick}')


def exchange(chat_id):
    """get currency."""
    cur.execute("select course_value from course where course_name='usd';")
    last_rate = cur.fetchone()[0]
    bot.send_message(chat_id=chat_id, text=f'Далар чичас па {last_rate} ₽')
