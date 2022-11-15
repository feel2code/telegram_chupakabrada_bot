from tabulate import tabulate

from ..conf import admin_chat
from ..connections import bot, cur


def send_statistics():
    cur.execute(
        f"""select * from (select '1' as Номер,
        'Всего отсылок' as Статистика,
        cast(count(stat_id) as text) as Количество from stats
        where date(st_date)=date(now()) and st_chat_id!='{admin_chat}'
        union
        select '2', 'Кол-во чатов', cast(count(foo.counting) as text)
        from (select count(st_chat_id) as counting from stats
        where date(st_date)=date(now()) and st_chat_id!='{admin_chat}'
        group by st_chat_id) as foo
        union
        select '3', 'По чатам', cast(count(st_chat_id) as text)
         from stats where date(st_date)=date(now())
        and st_chat_id!='{admin_chat}'
        group by st_chat_id
        union select '4', 'Дата', cast(date(st_date) as text) from
        stats where date(st_date)=date(now())
        and st_chat_id!='{admin_chat}'
        ) as foo
        order by Номер;""")
    bot.send_message(chat_id=admin_chat, text=tabulate(cur.fetchall()))
