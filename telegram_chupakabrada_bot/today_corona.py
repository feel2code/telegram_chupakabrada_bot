import requests
from bs4 import BeautifulSoup

from connections import bot


def coronavirus(chat: int):
    soup = BeautifulSoup(requests.get('https://стопкоронавирус.рф/information/').text, "html.parser")
    found = str(str(soup.select('cv-stats-virus')).split(':stats-data=')[1]).split(',')
    sick_change = str(found[1]).replace('"sickChange":"', '').replace('"', '')
    died_change = str(found[5]).replace('"diedChange":"', '').replace('"', '').replace(r'\u00a0', ' ')
    what_to_send = f'Корона тайм, зяблс. За сегодня в России:\nЗаболевших {sick_change} \nСмертей {died_change} \n'
    bot.send_message(chat_id=chat, text=what_to_send)
