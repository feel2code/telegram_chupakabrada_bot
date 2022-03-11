from connections import bot, cur


def zoo(message, sticker_family):
    cur.execute(f"SELECT sticker_id FROM {sticker_family}"
                f" order by random() limit 1; ")
    sticker_id = cur.fetchone()[0]
    bot.send_sticker(message.chat.id, sticker_id)
