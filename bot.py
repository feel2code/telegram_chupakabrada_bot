import telebot
import requests
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

k4 = ''
p4 = ''
m4 = ''
e4 = ''


def weather_kzn():
    global k4
    r = requests.get('http://api.openweathermap.org/data/2.5/weather?q=kazan&appid='+go_weather)
    k = r.json()
    k1 = k['main']
    k2 = k1['temp']
    k3 = int(k2 - 273)
    k4 = str(k3)
    return k4


def weather_spb():
    global p4
    r = requests.get('http://api.openweathermap.org/data/2.5/weather?id=498817&appid='+go_weather)
    p = r.json()
    p1 = p['main']
    p2 = p1['temp']
    p3 = int(p2 - 273)
    p4 = str(p3)
    return p4


def weather_msk():
    global m4
    r = requests.get('http://api.openweathermap.org/data/2.5/weather?q=moscow&appid='+go_weather)
    m = r.json()
    m1 = m['main']
    m2 = m1['temp']
    m3 = int(m2 - 273)
    m4 = str(m3)
    return m4


def weather_ekb():
    global e4
    r = requests.get('http://api.openweathermap.org/data/2.5/weather?id=1486209&appid='+go_weather)
    e = r.json()
    e1 = e['main']
    e2 = e1['temp']
    e3 = int(e2 - 273)
    e4 = str(e3)
    return e4


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
    global k4
    global p4
    global m4
    global e4
    if message.text == '/weather' or message.text == '/weather@chupakabrada_bot':
        weather_kzn()
        weather_spb()
        weather_msk()
        weather_ekb()
        bot.send_message(message.chat.id, 'Погода в Казани: '+k4+' по Цельсию.')
        bot.send_message(message.chat.id, 'Погода в Питере: ' + p4 + ' по Цельсию.')
        bot.send_message(message.chat.id, 'Погода в Москве: ' + m4 + ' по Цельсию.')
        bot.send_message(message.chat.id, 'Погода в Екатеринбурге: ' + e4 + ' по Цельсию.')
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
    elif msg in message_no:
        bot.send_message(message.chat.id, "Ну, как хаварица, на нет и кабылы нет.")
    elif msg in message_thanks:
        bot.send_message(message.chat.id, "Соси Пажилую Сасульку. А, ню да. Так расшифровываеца.")
    elif msg in message_who:
        bot.send_message(message.chat.id, 'А кто кто кто кто а ктооо???')
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAP-YWA2fmSUzgbH_bVtT8VOnEYSU80AAnsOAAIDKJlKdv4m3SZDnO4hBA')


# @bot.message_handler(content_types=["sticker"])
# def send_sticker(message):
    # sticker_id = message.sticker.file_id
    # bot.send_message(message.chat.id, sticker_id)

# @bot.message_handler(content_types=["text"])
# def chat_id(message):
#     if message.text == 'chat':
#         chat_id_var = message.chat.id
#         bot.send_message(message.chat.id, chat_id_var)


@bot.message_handler(content_types=['voice'])
def get_voice_messages(voice):
    bot.send_message(voice.chat.id, "Ничего не слышно, АЛО СВИТЛАНА????")


@bot.message_handler(content_types=['audio'])
def get_audio_messages(audio):
    bot.send_message(audio.chat.id, "ООО, эта деду нраица!")


bot.polling(none_stop=True, interval=0)
