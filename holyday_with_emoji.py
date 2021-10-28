import telebot
import requests
from bs4 import BeautifulSoup
from conf import *
from datetime import datetime
import pylightxl as xl


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
page = requests.get('https://ru.wikipedia.org/wiki/' + data)
soup = BeautifulSoup(page.text, "html.parser")
# for item in soup.select("li"):
#     today.append(item.get_text())

# for h in soup.find_all('h3'):
#     print(h.get('h3'))
found = soup.select('h3')

print(found)
# print(soup)
# bot.send_message(chat_id=chat, text=(today))
'''
index = today.index('6 Примечания')
db = xl.readxl(fn='countries.xlsx') #, ws='Table1')
for i in range(0, index + 1):
    today.pop(0)

# res = ' '.join([d.get(i, i) for i in a.split()])
# country = db.ws(ws='Sheet1').address(address='D' + str(1))

today = [word.replace('\xa0Греция\xa0', '🇬🇷') for word in today]
today = [word.replace('\xa0Украина\xa0', '🇺🇦') for word in today]
today = [word.replace('\xa0Чехословакия\xa0', '🇨🇿') for word in today]
today = [word.replace('\xa0Россия\n', '🇷🇺') for word in today]
# today[0] = ' ' + today[0]
case = str([word + '\n' for word in today])
case = case.replace(',', '')
case = case.replace('[', '')
case = case.replace(']', '')
case = case.replace('[', '')
case = case.replace("'", "")
case = case.replace(r"\n", "\n")
case = case.replace(r"уточнить", "")
case = case.replace(r"—", "")
case = case.replace(r".", "")
case = case.replace(r"Международный", "🌍 Международный")
for e in range(0, 250):
    case = case.replace(str(e), "")
head, sep, tail = case.partition('Православные')
print(head)
# bot.send_message(chat_id=chat, text=('Сиводня палучаица ' + str(datetime.now().date()) + ': \n' + head))
'''