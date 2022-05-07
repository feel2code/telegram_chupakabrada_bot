from datetime import datetime

from connections import conn_db, cur


def analytics(message):
    """analytics."""
    st_chat_id = f'{message.chat.id}'
    st_name = f'{message.from_user.first_name} {message.from_user.last_name}'
    st_nick = f'{message.from_user.username}'
    st_date = datetime.now()
    cur.execute(
        f"insert into stats (st_chat_id, st_name, st_nick, st_date) "
        f"values ('{st_chat_id}','{st_name}','{st_nick}','{st_date}');"
    )
    conn_db.commit()
