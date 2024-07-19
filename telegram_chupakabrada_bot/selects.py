import time
from datetime import datetime

from connections import SQLUtils, bot


def check(message, db_conn: SQLUtils):
    """Checking does message has any word in list from dictionary."""
    msg_check = message.text.lower().split()
    for word in msg_check:
        try:
            rec = db_conn.query(
                f"""select a.answer from questions as q
                    join answers a on q.ans_id=a.ans_id
                    where lower(q.question)={repr(word)};"""
            )[0]
        except IndexError:
            continue
        if not rec:
            continue
        rec = rec[0]
        bot.send_message(message.chat.id, rec)


def one_message(message, db_conn: SQLUtils):
    """sends message if any match was fetched from db."""
    try:
        fetched = db_conn.query(
            f"""select a.answer from answers a
                join messages m on m.ans_id=a.ans_id
                where msg_txt='{message.text.upper()}';"""
        )[0][0]
        bot.send_message(message.chat.id, fetched)
    except IndexError:
        pass


def simple_query(ans_id):
    """query from answers table."""
    db_conn = SQLUtils()
    return db_conn.query(f"select answer from answers where ans_id={ans_id};")[0][0]


def query(ans_id, chat_id, db_conn: SQLUtils):
    """send message to chat."""
    bot.send_message(
        chat_id=chat_id,
        text=db_conn.query(f"select answer from answers where ans_id={ans_id};"),
    )


def sticker_send(message):
    """send stickers to chat."""
    db_conn = SQLUtils()
    query(51, message.chat.id, db_conn)
    for stick_id in range(1, 10):
        bot.send_sticker(
            chat_id=message.chat.id,
            sticker=db_conn.query(
                f"select sticker from stickers where sticker_id={stick_id};"
            )[0][0],
        )
        time.sleep(0.200)


def zoo(message):
    """send sticker via animal-like-codeword to chat."""
    zoo_dict = {
        "/хрю": "pig_stickers",
        "/гав": "dog_stickers",
    }
    db_conn = SQLUtils()
    sticker_id = db_conn.query(
        f"""select sticker_id
            from {zoo_dict[message.text]} order by random() limit 1;"""
    )[0][0]
    bot.send_sticker(message.chat.id, sticker_id)


def roll(message):
    """roll someone in chat."""
    db_conn = SQLUtils()
    count = db_conn.query(
        f"""select count(1) from rolls
            where chat_id='{message.chat.id}'
            and cur_date='{datetime.today().strftime('%Y-%m-%d')}';"""
    )[0][0]
    if count == 0:
        nick = db_conn.query(
            f"""select * from (
                    select distinct st_nick from stats
                    where st_chat_id='{message.chat.id}' and st_nick != 'None'
                    ) as foo
                order by random() limit 1;"""
        )[0][0]
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
        )[0][0]
        bot.send_message(
            chat_id=message.chat.id, text=f"Великий рандом выбрал тебя, @{nick}"
        )


def rates_exchange(message):
    """usd currency rate."""
    ccy = "usd"
    return_mode = False
    if not isinstance(message, str):
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
        rate / (select rate from rates where ccy_iso3='{ccy}')
        from rates where ccy_iso3 = 'RUB'), 1);"""
        )[0][0]
    )
    return last_rate


def get_start(message):
    """sends start message."""
    db_conn = SQLUtils()
    bot.send_message(
        message.chat.id,
        db_conn.query("select start_text from start_q where start_id=1;")[0][0],
    )


def get_about(message):
    """sends message about author."""
    db_conn = SQLUtils()
    bot.send_message(
        message.chat.id,
        db_conn.query("select about_text from about where about_id=1;")[0][0],
    )


def get_quote(message):
    """sends quote."""
    db_conn = SQLUtils()
    bot.send_message(
        message.chat.id,
        db_conn.query("select quote_value from quotes order by random() limit 1;")[0][
            0
        ],
    )
