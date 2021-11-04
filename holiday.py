import telebot
import requests
from bs4 import BeautifulSoup
from conf import *
from datetime import datetime


day = datetime.now().day
month = datetime.now().month
m1 = 'января'
m2 = 'февраля'
m3 = 'марта'
m4 = 'апреля'
m5 = 'мая'
m6 = 'июня'
m7 = 'июля'
m8 = 'августа'
m9 = 'сентября'
m10 = 'октября'
m11 = 'ноября'
m12 = 'декабря'
data = ''
if month == 1:
    data = str(day) + '_' + m1
elif month == 2:
    data = str(day) + '_' + m2
elif month == 3:
    data = str(day) + '_' + m3
elif month == 4:
    data = str(day) + '_' + m4
elif month == 5:
    data = str(day) + '_' + m5
elif month == 6:
    data = str(day) + '_' + m6
elif month == 7:
    data = str(day) + '_' + m7
elif month == 8:
    data = str(day) + '_' + m8
elif month == 9:
    data = str(day) + '_' + m9
elif month == 10:
    data = str(day) + '_' + m10
elif month == 11:
    data = str(day) + '_' + m11
elif month == 12:
    data = str(day) + '_' + m12


chat = '-1001173893696'
today = []
bot = telebot.TeleBot(name)
page = requests.get('https://ru.wikipedia.org/wiki/' + 'Категория:Праздники_' + data)
soup = BeautifulSoup(page.text, "html.parser")
for item in soup.select("li"):
    today.append(item.get_text())
index = today.index('Праздники' + data.replace(str(day) + '_', ' '))
i = index
while len(today) != i:
    today.pop(index)
today[0] = ' ' + today[0]
case = str([word + '\n' for word in today])
case1 = case.replace(',', '')
case2 = case1.replace('[', '')
case3 = case2.replace(']', '')
case4 = case3.replace('[', '')
case5 = case4.replace("'", "")
case6 = case5.replace(r"\n", "\n")
bot.send_message(chat_id=chat, text=('Сиводня палучаица ' + str(datetime.now().date()) + ': \n' + case6))
