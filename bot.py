import telebot
from conf import *


bot = telebot.TeleBot(name)

hi = 'доброе добрае доброго хай хай, хаай хааай'
ass = 'жопа'
message_lol = ['ХЕХ', 'АХАХАХ', 'АХАХАХАХ', 'ЛОЛ', 'ХАХА']
message_plus = ['+', '++', '+++', '++++']
message_aga = ['АГА']
message_steel = ['ЖЕСТЬ']
message_wtf = [')', '))', ')))', '))))', ')))))']
message_sad = ['(', '((', '(((', '((((', '(((((']
message_a = ['А', 'АА', 'ААА', 'АААА']
message_who = ['ХТО', 'КТО', 'КТО?', 'ХТО?']
message_no = ['НЕ', 'НЕТ', 'НЕА', 'НЕТ(', 'НЕТ)']
message_thanks = ['СПС', 'SPS']
who_is_bot = 'каво'
abba = 'абоба абобус амогус аабоба'
note = 'ля ля, ляя ляяя'


def check(message, diction, answer):
    msg_check = message.text.upper().split()
    dictionary = diction.upper().split()
    b = len(msg_check)
    i = 0
    while i < b:
        if msg_check[i] in dictionary:
            bot.send_message(message.chat.id, answer)
            i += 1
        else:
            i += 1


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == '/sticker':
        bot.send_message(message.chat.id, r'Ну вот тебе наклеечки, вот,'
                                          r'пожалуйста, https://t.me/addstickers/Jessieamstaff')
    if message.text == '/start':
        bot.send_message(message.chat.id, r'Я тебе, шо, космонавт, чи шо? Добавляй в группу меня, скатабаза такая.')
    if message.text == '/belching':
        bot.send_message(message.chat.id, r'БУЭЭЭ')
    msg = message.text.upper()
    check(message, hi, 'Хааааааай зяблс энд хай литл бэби бон')
    check(message, who_is_bot, 'Каво?')
    check(message, abba, 'А Б О Б А')
    check(message, 'о', 'Шо ти окаешь, девачка?')
    check(message, 'общем', 'В общем и целом, ага, ню да.')
    check(message, ass, 'Кто? Я? А может быть ТЫ? А?')
    check(message, note, 'Ля, какая!')
    if msg in message_lol:
        bot.send_message(message.chat.id, "Пожилая скумбрия на связи. Зарофлю любого лола.")
    elif msg in message_plus:
        bot.send_message(message.chat.id, "Я тебе плюсану па галаве чичас кулаком")
    elif msg in message_aga:
        bot.send_message(message.chat.id, "Оооо, ну эта бан палучаица")
    elif msg in message_steel:
        bot.send_message(message.chat.id, "КХХХХтьфу")
    elif msg in message_wtf:
        bot.send_message(message.chat.id, "Все гиги гага, смешно да? А тебе не стыдно, не? Ай-яй-яй-яй-яй. Тьфу.")
    elif msg in message_sad:
        bot.send_message(message.chat.id, "Абидна да? хихихих")
    elif msg in message_a:
        bot.send_message(message.chat.id, "А?")
    elif msg in message_who:
        bot.send_message(message.chat.id, "Каво?")
    elif msg in message_no:
        bot.send_message(message.chat.id, "Ну, как хаварица, на нет и кабылы нет.")
    elif msg in message_thanks:
        bot.send_message(message.chat.id, "Соси Пажилую Сасульку. А, ню да. Так расшифровываеца.")


@bot.message_handler(content_types=['voice'])
def get_voice_messages(sound):
    bot.send_message(sound.chat.id, "Ничего не слышно, АЛО СВИТЛАНА????")


@bot.message_handler(content_types=['audio'])
def get_audio_messages(audio):
    bot.send_message(audio.chat.id, "ООО, эта деду нраица!")


bot.polling(none_stop=True, interval=0)
