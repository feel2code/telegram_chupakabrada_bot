from datetime import datetime

from connections import SQLUtils


def analytics(message, db_conn: SQLUtils):
    """analytics."""
    st_chat_id = message.chat.id
    st_name = f"{message.from_user.first_name} {message.from_user.last_name}"
    st_nick = message.from_user.username
    st_date = datetime.now()
    db_conn.mutate(
        f"""insert into stats (st_chat_id, st_name, st_nick, st_date)
            values ('{st_chat_id}','{st_name}','{st_nick}','{st_date}');"""
    )
