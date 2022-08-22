import time
from datetime import datetime

from connections import bot, conn_db, cur
from constants import GODZILLA


# checking does message has any word in list from dictionary
def check(message):
    msg_check = message.text.upper().split()
    i = 0
    while i < len(msg_check):
        quest = msg_check[i]
        try:
            cur.execute(f"""select a.answer from questions as q join answers a on q.ans_id=a.ans_id
                                     where upper(q.question)='{quest}';""")
            rec = cur.fetchone()
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
                i += 1
            else:
                bot.send_message(message.chat.id, rec)
                i += 1
        except IndexError:
            i += 1


def one_message(message):
    cur.execute('select count(1) from messages')
    msg_length = cur.fetchone()[0]
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


def roll(chat_id):
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
