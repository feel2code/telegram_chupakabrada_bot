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
sochi = ''


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


def weather_sochi():
    global sochi
    r = requests.get('https://api.openweathermap.org/data/2.5/weather?id=491422&appid='+go_weather)
    b = r.json()
    sochi1 = b['main']
    sochi = str(int(sochi1['temp'] - 273))
    return sochi


weather_kzn()
weather_spb()
weather_msk()
weather_ekb()
weather_batumi()
weather_sochi()
if chat == '-1001173893696':
    what_to_send = 'Ну шо, с добрим утречком всех, мои зяблики, маи родненькие!' \
                   ' \n Вот вам ваша пагода па расписанию, палучаица:'
else:
    what_to_send = 'Вот вам ваша пагода, блин, ню да, палучаица:'
what_to_send += ('\n ' + k4 + ' °C Казань \n ' + p4)
what_to_send += (' °C Питер \n ' + m4 + ' °C Москва \n ' + e4 + ' °C Екб \n ')
what_to_send += (b4 + ' °C Батуми \n ')
what_to_send += (sochi + ' °C Сочи \n ')
bot.send_message(chat_id=chat, text=what_to_send)
