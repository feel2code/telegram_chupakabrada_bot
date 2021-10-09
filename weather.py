import telebot
import requests
from conf import *

bot = telebot.TeleBot(name)
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


chat = '-1001173893696'
bot.send_message(chat_id=chat, text='Вот вам ваша пагода па расписанию, палучаица:')
weather_kzn()
weather_spb()
weather_msk()
weather_ekb()
bot.send_message(chat_id=chat, text='Погода в Казани: ' + k4 + ' по Цельсию.')
bot.send_message(chat_id=chat, text='Погода в Питере: ' + p4 + ' по Цельсию.')
bot.send_message(chat_id=chat, text='Погода в Москве: ' + m4 + ' по Цельсию.')
bot.send_message(chat_id=chat, text='Погода в Екатеринбурге: ' + e4 + ' по Цельсию.')