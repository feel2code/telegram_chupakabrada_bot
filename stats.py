import telebot
from conf import name, conn
import psycopg2
from tabulate import tabulate

bot = telebot.TeleBot(name)
conn_db = psycopg2.connect(conn)
cur = conn_db.cursor()
cur.execute("select * from (select '1' as Номер, "
            "'Всего отсылок' as Статистика, "
            "cast(count(stat_id) as text) as Количество from stats "
            "where date(st_date)=date(now()) "
            "union "
            "select '2', 'Кол-во чатов', cast(count(foo.counting) as text) "
            "from (select count(st_chat_id) as counting from stats "
            "where date(st_date)=date(now())"
            "group by st_chat_id) as foo "
            "union "
            "select '3', 'По чатам', cast(count(st_chat_id) as text)"
            " from stats where date(st_date)=date(now()) "
            "group by st_chat_id "
            "union select '4', 'Дата', cast(date(st_date) as text) from "
            "stats where date(st_date)=date(now()) "
            ") as foo "
            "order by Номер ")
records = cur.fetchall()
what_to_send = (tabulate(records))
chat = "442295142"
bot.send_message(chat_id=chat, text=what_to_send)
