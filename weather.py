import telebot
import requests
from conf import *
from sys import argv

script, chat = argv
bot = telebot.TeleBot(name)
k4 = ''
p4 = ''
m4 = ''
e4 = ''
b4 = ''
t4 = ''


def weather_kzn():
    global k4
    r = requests.get('https://api.openweathermap.org/data/2.5/weather?q=kazan&appid='+go_weather)
    k = r.json()
    k1 = k['main']
    k2 = k1['temp']
    k3 = int(k2 - 273)
    k4 = str(k3)
    return k4


def weather_spb():
    global p4
    r = requests.get('https://api.openweathermap.org/data/2.5/weather?id=498817&appid='+go_weather)
    p = r.json()
    p1 = p['main']
    p2 = p1['temp']
    p3 = int(p2 - 273)
    p4 = str(p3)
    return p4


def weather_msk():
    global m4
    r = requests.get('https://api.openweathermap.org/data/2.5/weather?q=moscow&appid='+go_weather)
    m = r.json()
    m1 = m['main']
    m2 = m1['temp']
    m3 = int(m2 - 273)
    m4 = str(m3)
    return m4


def weather_ekb():
    global e4
    r = requests.get('https://api.openweathermap.org/data/2.5/weather?id=1486209&appid='+go_weather)
    e = r.json()
    e1 = e['main']
    e2 = e1['temp']
    e3 = int(e2 - 273)
    e4 = str(e3)
    return e4


def weather_batumi():
    global b4
    r = requests.get('https://api.openweathermap.org/data/2.5/weather?id=615532&appid='+go_weather)
    b = r.json()
    b1 = b['main']
    b2 = b1['temp']
    b3 = int(b2 - 273)
    b4 = str(b3)
    return b4


def weather_tbilisi():
    global t4
    r = requests.get('https://api.openweathermap.org/data/2.5/weather?id=611717&appid='+go_weather)
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
full_weather_dict = {k4:'Казани',
p4: 'Питере', m4: 'Москве', e4: 'Екб', b4: 'Батуми',
t4:'Тбилиси'}
inverted_weather_dict = {'Казани':k4,
'Питере':p4, 'Москве':m4 , 'Екб':e4 , 'Батуми':b4,
'Тбилиси':t4}

# max temp
max_weather = max(full_weather_list)
# min temp
min_weather = min(full_weather_list)


what_to_send = ('Ну шо, с добрим утречком всех, мои зяблики, маи родненькие!\n\n'
                'Вот вам ваша пагода па расписанию, палучаица:\n')

what_to_send += ('\n' + k4 + ' °C · Казань')
if full_weather_dict[str(min_weather)] == 'Казань': what_to_send += '❄️'
elif full_weather_dict[str(max_weather)] == 'Казань': what_to_send += '🔥'

what_to_send += ('\n' + p4 + ' °C · Питер')
if full_weather_dict[str(min_weather)] == 'Питер': what_to_send += '❄️'
elif full_weather_dict[str(max_weather)] == 'Питер': what_to_send += '🔥'

what_to_send += ('\n' + m4 + ' °C · Москва')
if full_weather_dict[str(min_weather)] == 'Москва': what_to_send += '❄️'
elif full_weather_dict[str(max_weather)] == 'Москва': what_to_send += '🔥'

what_to_send += ('\n' + e4 + ' °C · Екб')
if full_weather_dict[str(min_weather)] == 'Екб': what_to_send += '❄️'
elif full_weather_dict[str(max_weather)] == 'Екб': what_to_send += '🔥'

what_to_send += ('\n' + b4 + ' °C · Батуми')
if full_weather_dict[str(min_weather)] == 'Батуми': what_to_send += '❄️'
elif full_weather_dict[str(max_weather)] == 'Батуми': what_to_send += '🔥'

what_to_send += ('\n' + t4 + ' °C · Тбилиси')
if full_weather_dict[str(min_weather)] == 'Тбилиси': what_to_send += '❄️'
elif full_weather_dict[str(max_weather)] == 'Тбилиси': what_to_send += '🔥'

bot.send_message(chat_id=chat, text=what_to_send)
