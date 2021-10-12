import telebot
import requests
from bs4 import BeautifulSoup
from conf import *
from datetime import datetime

chat = '-1001173893696'
today = []
bot = telebot.TeleBot(name)
page = requests.get('https://sptoday.ru/kakoj-segodnya-prazdnik/')
soup = BeautifulSoup(page.text, "html.parser")
holiday_today = soup.findAll('div', class_='prazdnik')
for data in holiday_today:
    if data.find('li') is not None:
        today.append(data.text)
today_is = str(today)
today_is1 = ((today_is.replace(r'\r', ' ')).replace(r'\n', ' ').replace('ufeff', ' '))
today_is2 = today_is1.replace("\\", " ")
today_is3 = today_is2.replace("['", " ")
today_is4 = today_is3.replace("']", " ")
today_is5 = today_is4.replace('                         ', '')
head, sep, tail = today_is5.partition('Церковные')
bot.send_message(chat_id=chat, text=('Сиводня палучаица ' + str(datetime.now().date()) + '\n' + str(head)))
