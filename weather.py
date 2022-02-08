import telebot
import requests
from conf import *
from sys import argv

script, chat = argv
bot = telebot.TeleBot(name)


def weather(id: str) -> str:
    requestings = requests.get(
        'https://api.openweathermap.org/data/2.5/weather?' + id +
        (
            '&appid=' + go_weather
        )
    ).json()
    temp_farenheit = (requestings['main'])['temp']
    temp_celsius = str(int(temp_farenheit - 273))
    return temp_celsius


k4 = weather('q=kazan')
p4 = weather('id=498817')
m4 = weather('q=moscow')
e4 = weather('id=1486209')
b4 = weather('id=615532')
t4 = weather('id=611717')

# find max and min weather in cities list
full_weather_list = [k4, p4, m4, e4, b4, t4]
full_weather_list = [int(item) for item in full_weather_list]
full_weather_dict = {k4: 'Казань', p4: 'Питер',
                     m4: 'Москва', e4: 'Екб',
                     b4: 'Батуми', t4: 'Тбилиси'}

# max/min temp
max_weather = max(full_weather_list)
min_weather = min(full_weather_list)

what_to_send = (
    'Ну шо, с добрим утречком всех, мои зяблики, маи родненькие!\n\n'
    'Вот вам ваша пагода па расписанию, палучаица:\n')


def weather_send(temp: str):
    '''Checking max or min temp and send emoji near temp'''
    global what_to_send
    temp = str(temp)
    temp_send = str(temp)
    if int(temp) >= 0 and int(temp) < 10:
        temp_send = temp.replace(temp, '  ' + temp)
    elif int(temp) < 0 and int(temp) > - 10:
        temp_send = temp.replace(temp, ' ' + temp)
    elif int(temp) > 10:
        temp_send = temp.replace(temp, ' ' + temp)
    what_to_send += ('\n' + temp_send + ' °C · ' + full_weather_dict[temp])
    if full_weather_dict[str(min_weather)] == full_weather_dict[temp]:
        what_to_send += ' ❄️'
    elif full_weather_dict[str(max_weather)] == full_weather_dict[temp]:
        what_to_send += ' 🔥'


for city_weather in full_weather_list:
    weather_send(city_weather)

bot.send_message(chat_id=chat, text=what_to_send)
