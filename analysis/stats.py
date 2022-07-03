from tabulate import tabulate

from conf import admin_chat
from connections import bot, cur


def send_statistics():
    cur.execute(
        f"select * from (select '1' as Номер, "
        f"'Всего отсылок' as Статистика, "
        f"cast(count(stat_id) as text) as Количество from stats "
        f"where date(st_date)=date(now()) and st_chat_id!='{admin_chat}' "
        f"union "
        f"select '2', 'Кол-во чатов', cast(count(foo.counting) as text) "
        f"from (select count(st_chat_id) as counting from stats "
        f"where date(st_date)=date(now()) and st_chat_id!='{admin_chat}' "
        f"group by st_chat_id) as foo "
        f"union "
        f"select '3', 'По чатам', cast(count(st_chat_id) as text)"
        f" from stats where date(st_date)=date(now()) "
        f"and st_chat_id!='{admin_chat}' "
        f"group by st_chat_id "
        f"union select '4', 'Дата', cast(date(st_date) as text) from "
        f"stats where date(st_date)=date(now()) "
        f"and st_chat_id!='{admin_chat}' "
        f") as foo "
        f"order by Номер ")
    records = cur.fetchall()
    what_to_send = (tabulate(records))
    bot.send_message(chat_id=admin_chat, text=what_to_send)
