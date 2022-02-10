import telebot
import requests
from bs4 import BeautifulSoup
from conf import name
from sys import argv

script, chat = argv

bot = telebot.TeleBot(name)
page = requests.get('https://стопкоронавирус.рф/information/')
soup = BeautifulSoup(page.text, "html.parser")
found = soup.select('cv-stats-virus')
found = str(found).split(':stats-data=')
found = str(found[1]).split(',')
sickChange = str(found[1]).replace('"sickChange":"', '')
sickChange = sickChange.replace('"', '')
diedChange = str(found[5]).replace('"diedChange":"', '')
diedChange = diedChange.replace('"', '')
diedChange = diedChange.replace(r'\u00a0', ' ')
what_to_send = 'Корона тайм зяблс. За сегодня в России: \n' \
               'Заболевших ' + sickChange + ' \n' \
               'Смертей ' + diedChange + ' \n'
bot.send_message(chat_id=chat, text=what_to_send)
