import telebot
import requests
from conf import *
from sys import argv

script, chat = argv
bot = telebot.TeleBot(name)
weather_url = 'https://api.openweathermap.org/data/2.5/weather?'


def weather(id: str) -> str:
    requestings = requests.get(
        'https://api.openweathermap.org/data/2.5/weather?' + id +
        (
            '&appid=' + go_weather
        )
    ).json()
    temp_farenheit = (requestings['main'])['temp']
    returned_temp = str(int(temp_farenheit - 273))
    return returned_temp


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


def weather_send(temp, city) -> None:
    '''Checking max or min temp and send emoji near temp'''
    global what_to_send
    if int(temp) >= 0 and int(temp) < 10:
        temp = temp.replace(temp, ' ' + temp)
    what_to_send += ('\n' + temp + ' °C · ' + city)
    if full_weather_dict[str(min_weather)] == city:
        what_to_send += ' ❄️'
    elif full_weather_dict[str(max_weather)] == city:
        what_to_send += ' 🔥'


weather_send(k4, full_weather_dict[k4])
weather_send(p4, full_weather_dict[p4])
weather_send(m4, full_weather_dict[m4])
weather_send(e4, full_weather_dict[e4])
weather_send(b4, full_weather_dict[b4])
weather_send(t4, full_weather_dict[t4])

bot.send_message(chat_id=chat, text=what_to_send)
