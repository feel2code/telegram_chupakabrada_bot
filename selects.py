import time
from constants import GODZILLA
from connections import bot, cur


# checking does message has any word in list from dictionary
def check(message):
    msg_check = message.text.upper().split()
    i = 0
    while i < len(msg_check):
        quest = msg_check[i]
        try:
            cur.execute(
                f"SELECT a.answer FROM questions as q join answers a on "
                f"q.ans_id=a.ans_id where upper(q.question)='{quest}' "
            )
            rec = (cur.fetchall()[0])[0]
            if rec == GODZILLA:
                rec = ''
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
    msg_length = (cur.fetchall()[0])[0]
    cur.execute("SELECT msg_txt FROM messages")
    msg_db = cur.fetchall()
    msg_list = []
    for i in range(0, msg_length):
        msg_list.append((msg_db[i])[0])
    if message.text.upper() in msg_list:
        cur.execute(f"SELECT a.answer FROM answers a join messages m on "
                    f"m.ans_id=a.ans_id where "
                    f"msg_txt='{message.text.upper()}'")
        records = cur.fetchone()[0]
        bot.send_message(message.chat.id, records)


def simple_query(ans_id):
    '''query from answers table'''
    cur.execute(f"SELECT answer FROM answers where ans_id={ans_id}")
    return cur.fetchone()[0]


def query(ans_id, chat_id):
    '''send message to chat'''
    bot.send_message(chat_id=chat_id, text=simple_query(ans_id))


def sticker_send(chat_id):
    query(51, chat_id)
    for stick_id in range(1, 10):
        cur.execute(f"SELECT sticker FROM stickers "
                    f"where sticker_id={stick_id} ")
        records = cur.fetchone()[0]
        bot.send_sticker(chat_id=chat_id, data=records)
        time.sleep(0.200)
