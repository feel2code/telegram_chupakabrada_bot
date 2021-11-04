import telebot
import requests
from bs4 import BeautifulSoup
from conf import *


chat = '-1001173893696'
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
what_to_send = 'Корона тайм зяблс. За сегодня в России: \n' \
               'Заболевших ' + sickChange + ' \n' \
               'Смертей ' + diedChange + ' \n'
bot.send_message(chat_id=chat, text=what_to_send)

'''
# данные за сутки
found = str(found).replace("[<cv-stats-virus :charts-data='[", '')
found = found.replace("'></cv-stats-virus>", '')
found = found.split(',')
while len(found) != 4:
    found.pop(4)
sick = str(found[1]).replace('"sick":', '')
healed = str(found[2]).replace('"healed":', '')
died = str(found[3]).replace('"died":', '')
died = died.replace('}', '')
'''
