import telebot
import requests
from conf import *
from sys import argv

script, chat = argv
bot = telebot.TeleBot(name)
weather_url = 'https://api.openweathermap.org/data/2.5/weather?'
k4 = ''
p4 = ''
m4 = ''
e4 = ''
b4 = ''
t4 = ''


def weather_kzn():
    global k4
    r = requests.get(weather_url + 'q=kazan&appid=' + go_weather)
    k = r.json()
    k1 = k['main']
    k2 = k1['temp']
    k3 = int(k2 - 273)
    k4 = str(k3)
    return k4


def weather_spb():
    global p4
    r = requests.get(weather_url + 'id=498817&appid=' + go_weather)
    p = r.json()
    p1 = p['main']
    p2 = p1['temp']
    p3 = int(p2 - 273)
    p4 = str(p3)
    return p4


def weather_msk():
    global m4
    r = requests.get(weather_url + 'q=moscow&appid=' + go_weather)
    m = r.json()
    m1 = m['main']
    m2 = m1['temp']
    m3 = int(m2 - 273)
    m4 = str(m3)
    return m4


def weather_ekb():
    global e4
    r = requests.get(weather_url + 'id=1486209&appid=' + go_weather)
    e = r.json()
    e1 = e['main']
    e2 = e1['temp']
    e3 = int(e2 - 273)
    e4 = str(e3)
    return e4


def weather_batumi():
    global b4
    r = requests.get(weather_url + 'id=615532&appid='+go_weather)
    b = r.json()
    b1 = b['main']
    b2 = b1['temp']
    b3 = int(b2 - 273)
    b4 = str(b3)
    return b4


def weather_tbilisi():
    global t4
    r = requests.get(weather_url + 'id=611717&appid='+go_weather)
    t = r.json()
    t1 = t['main']
    t2 = t1['temp']
    t3 = int(t2 - 273)
    t4 = str(t3)
    return t4


weather_kzn()
weather_spb()
weather_msk()
weather_ekb()
weather_batumi()
weather_tbilisi()

# find max and min weather in cities list
full_weather_list = [k4, p4, m4, e4, b4, t4]
full_weather_list = [int(item) for item in full_weather_list]
# full_weather_list = [k4, p4, m4, e4, b4, t4]
full_weather_dict = {k4: 'Казань', p4: 'Питер',
                     m4: 'Москва', e4: 'Екб',
                     b4: 'Батуми', t4: 'Тбилиси'}
inverted_weather_dict = {'Казань': k4, 'Питер': p4,
                         'Москва': m4, 'Екб': e4,
                         'Батуми': b4, 'Тбилиси': t4}

# max temp
max_weather = max(full_weather_list)
# min temp
min_weather = min(full_weather_list)


what_to_send = (
    'Ну шо, с добрим утречком всех, мои зяблики, маи родненькие!\n\n'
    'Вот вам ваша пагода па расписанию, палучаица:\n')

# adding temp variables
tk4 = k4
tp4 = p4
tm4 = m4
te4 = e4
tb4 = b4
tt4 = t4

if int(k4) > 0 and int(k4) < 10: tk4 = k4.replace(k4, ' ' + k4)
what_to_send += ('\n' + tk4 + ' °C · Казань')
if full_weather_dict[str(min_weather)] == 'Казань': what_to_send += ' ❄️'
elif full_weather_dict[str(max_weather)] == 'Казань': what_to_send += ' 🔥'

if int(p4) > 0 and int(p4) < 10: tp4 = p4.replace(p4, ' ' + p4)
what_to_send += ('\n' + tp4 + ' °C · Питер')
if full_weather_dict[str(min_weather)] == 'Питер': what_to_send += ' ❄️'
elif full_weather_dict[str(max_weather)] == 'Питер': what_to_send += ' 🔥'

if int(m4) > 0 and int(m4) < 10: tm4 = m4.replace(m4, ' ' + m4)
what_to_send += ('\n' + tm4 + ' °C · Москва')
if full_weather_dict[str(min_weather)] == 'Москва': what_to_send += ' ❄️'
elif full_weather_dict[str(max_weather)] == 'Москва': what_to_send += ' 🔥'

if int(e4) > 0 and int(e4) < 10: te4 = e4.replace(e4, ' ' + e4)
what_to_send += ('\n' + te4 + ' °C · Екб')
if full_weather_dict[str(min_weather)] == 'Екб': what_to_send += ' ❄️'
elif full_weather_dict[str(max_weather)] == 'Екб': what_to_send += ' 🔥'

if int(b4) > 0 and int(b4) < 10: tb4 = b4.replace(b4, ' ' + b4)
what_to_send += ('\n' + tb4 + ' °C · Батуми')
if full_weather_dict[str(min_weather)] == 'Батуми': what_to_send += ' ❄️'
elif full_weather_dict[str(max_weather)] == 'Батуми': what_to_send += ' 🔥'

if int(t4) > 0 and int(t4) < 10: tt4 = t4.replace(t4, ' ' + t4)
what_to_send += ('\n' + tt4 + ' °C · Тбилиси')
if full_weather_dict[str(min_weather)] == 'Тбилиси': what_to_send += ' ❄️'
elif full_weather_dict[str(max_weather)] == 'Тбилиси': what_to_send += ' 🔥'


bot.send_message(chat_id=chat, text=what_to_send)
