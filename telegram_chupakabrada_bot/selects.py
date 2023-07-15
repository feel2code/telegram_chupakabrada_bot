import time
from datetime import datetime

from connections import bot, MySQLUtils
from constants import GODZILLA


def check(message, db_conn: MySQLUtils):
    """Checking does message has any word in list from dictionary."""
    msg_check = message.text.upper().split()
    for word in msg_check:
        try:
            rec = db_conn.query(
                f"""select a.answer from questions as q join answers a on q.ans_id=a.ans_id
                    where upper(q.question)={word.__repr__()};"""
            )[0]
        except IndexError:
            continue
        if not rec:
            continue
        else:
            rec = rec[0]
        if rec == GODZILLA:
            query(103, message.chat.id, db_conn)
            time.sleep(1)
            i_count = 104
            while i_count < 111:
                query(i_count, message.chat.id, db_conn)
                time.sleep(0.100)
                i_count += 1
            i_count = 109
            while i_count > 103:
                query(i_count, message.chat.id, db_conn)
                time.sleep(0.100)
                i_count = i_count - 1
            continue
        else:
            bot.send_message(message.chat.id, rec)


def one_message(message, db_conn: MySQLUtils):
    try:
        fetched = db_conn.query(f"""select a.answer from answers a
                                    join messages m on m.ans_id=a.ans_id
                                    where msg_txt='{message.text.upper()}';""")[0][0]
        bot.send_message(message.chat.id, fetched)
    except IndexError:
        pass


def simple_query(ans_id):
    """query from answers table."""
    db_conn = MySQLUtils()
    return db_conn.query(f"select answer from answers where ans_id={ans_id};")[0][0]


def query(ans_id, chat_id, db_conn: MySQLUtils):
    """send message to chat."""
    bot.send_message(chat_id=chat_id,
                     text=db_conn.query(f"select answer from answers where ans_id={ans_id};"))


def sticker_send(chat_id):
    """send stickers to chat."""
    db_conn = MySQLUtils()
    query(51, chat_id, db_conn)
    for stick_id in range(1, 10):
        bot.send_sticker(chat_id=chat_id,
                         data=db_conn.query(f"select sticker from stickers where sticker_id={stick_id};")[0][0])
        time.sleep(0.200)


def zoo(message, sticker_family, db_conn: MySQLUtils):
    """send sticker via animal-like-codeword to chat."""
    sticker_id = db_conn.query(f"select sticker_id from {sticker_family} order by rand() limit 1;")[0][0]
    bot.send_sticker(message.chat.id, sticker_id)


def roll(chat_id: int):
    """roll someone in chat."""
    db_conn = MySQLUtils()
    count = db_conn.query(
        f"select count(1) from rolls where chat_id='{chat_id}' and cur_date='{datetime.today().strftime('%Y-%m-%d')}';"
    )[0][0]
    if count == 0:
        nick = db_conn.query(f"""select * from (select distinct st_nick from stats
                                       where st_chat_id='{chat_id}' and st_nick != 'None') as foo
                        order by rand() limit 1;""")[0][0]
        bot.send_message(chat_id=chat_id, text=f'Великий рандом выбрал тебя, @{nick}')
        db_conn.mutate(f"insert into rolls values('{nick}', '{chat_id}', '{datetime.today().strftime('%Y-%m-%d')}');")
    else:
        nick = db_conn.query(
            f"select nick from rolls where chat_id='{chat_id}' and cur_date='{datetime.today().strftime('%Y-%m-%d')}';"
        )[0][0]
        bot.send_message(chat_id=chat_id, text=f'Великий рандом выбрал тебя, @{nick}')


def usd_exchange(chat_id):
    """usd currency rate."""
    db_conn = MySQLUtils()
    last_rate = db_conn.query("select course_value from course where course_name='usd';")[0][0]
    bot.send_message(chat_id=chat_id, text=f'Далар чичас па {last_rate} ₽')


def gel_exchange(chat_id):
    """gel currency rate."""
    db_conn = MySQLUtils()
    last_rate = db_conn.query("select course_value from course where course_name='gel';")[0][0]
    bot.send_message(chat_id=chat_id, text=f'Ларики чичас па {last_rate} ₽')
