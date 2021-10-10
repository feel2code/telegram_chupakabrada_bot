# auxiliary.py
'''

# for getting sticker id
@bot.message_handler(content_types=["sticker"])
def send_sticker(message):
    sticker_id = message.sticker.file_id
    bot.send_message(message.chat.id, sticker_id)

# for getting chat id
@bot.message_handler(content_types=["text"])
def chat_id(message):
    if message.text == 'chat':
        chat_id_var = message.chat.id
        bot.send_message(message.chat.id, chat_id_var)

'''
