import random
import time
from datetime import datetime

from connections import SQLUtils, bot


def check(message):
    """Checking does message has any word in list from dictionary."""
    db_conn = SQLUtils()
    msg_check = message.text.lower().split()
    for word in msg_check:
        rec = db_conn.query(
            f"""select a.answer from questions as q
                join answers a on q.ans_id=a.ans_id
                where lower(q.question)={repr(word)};"""
        )
        if not rec:
            continue
        bot.send_message(message.chat.id, rec)


def one_message(message):
    """sends message if any match was fetched from db."""
    db_conn = SQLUtils()
    fetched = db_conn.query(
        f"""select a.answer from answers a
            join messages m on m.ans_id=a.ans_id
            where msg_txt='{message.text.upper()}';"""
    )
    if fetched:
        bot.send_message(message.chat.id, fetched)


def simple_query(ans_id):
    """query from answers table."""
    db_conn = SQLUtils()
    return db_conn.query(f"select answer from answers where ans_id={ans_id};")


def query(ans_id, chat_id):
    """send message to chat."""
    bot.send_message(chat_id=chat_id, text=simple_query(ans_id))


def sticker_send(message):
    """send stickers to chat."""
    db_conn = SQLUtils()
    query(51, message.chat.id)
    stickers = db_conn.query("select sticker from stickers;")
    for stick_id in stickers:
        bot.send_sticker(chat_id=message.chat.id, sticker=stick_id)
        time.sleep(0.200)


def roll(message):
    """roll someone in chat."""
    db_conn = SQLUtils()
    count = db_conn.query(
        f"""select count(1) from rolls
            where chat_id='{message.chat.id}'
            and cur_date='{datetime.today().strftime('%Y-%m-%d')}';"""
    )
    if count == 0:
        nick = db_conn.query(
            f"""select * from (
                    select distinct st_nick from stats
                    where st_chat_id='{message.chat.id}' and st_nick != 'None'
                    ) as foo
                order by random() limit 1;"""
        )
        bot.send_message(
            chat_id=message.chat.id, text=f"Великий рандом выбрал тебя, @{nick}"
        )
        db_conn.mutate(
            f"""insert into rolls
                values('{nick}', '{message.chat.id}',
                       '{datetime.today().strftime('%Y-%m-%d')}');"""
        )
    else:
        nick = db_conn.query(
            f"""select nick from rolls
                where chat_id='{message.chat.id}'
                and cur_date='{datetime.today().strftime('%Y-%m-%d')}';"""
        )
        bot.send_message(
            chat_id=message.chat.id, text=f"Великий рандом выбрал тебя, @{nick}"
        )


def rates_exchange(message):
    """usd currency rate."""
    ccy = "usd"
    return_mode = False
    if not isinstance(message, int):
        ccy = message.text.split(" ")[0][1:].replace("@chupakabrada_bot", "")
    else:
        return_mode = True
    last_rate = get_rates_from_db(ccy)
    ccy_map = {"usd": "Далары", "gel": "Ларики"}
    result_message = f"{ccy_map[ccy]} чичас па {last_rate} ₽"
    if return_mode:
        return result_message
    bot.send_message(chat_id=message.chat.id, text=result_message)
    return None


def get_rates_from_db(ccy):
    """get last updated rate from db"""
    db_conn = SQLUtils()
    last_rate = int(
        db_conn.query(
            f"""select round((
        select
        rate / (select rate from rates where lower(ccy_iso3)='{ccy}')
        from rates where ccy_iso3 = 'RUB'), 1);"""
        )
    )
    return last_rate


def get_start(message):
    """sends start message."""
    db_conn = SQLUtils()
    bot.send_message(
        message.chat.id,
        db_conn.query("select start_text from start_q where start_id=1;"),
    )


def get_about(message):
    """sends message about author."""
    db_conn = SQLUtils()
    bot.send_message(
        message.chat.id,
        db_conn.query("select about_text from about where about_id=1;"),
    )


def get_quote(message):
    """sends quote."""
    db_conn = SQLUtils()
    bot.send_message(
        message.chat.id,
        db_conn.query("select quote_value from quotes order by random() limit 1;"),
    )


def check_sending_random_voice(message):
    """Check if random voice message should be sent."""
    db_conn = SQLUtils()
    hardness = db_conn.query(
        f"select hardness from markov where chat_id={message.chat.id}"
    )
    if hardness:
        if int(hardness) < 9:
            if random.randint(1, 5) == 1:
                return True
    return False
