import requests
from bs4 import BeautifulSoup

from connections import bot


def coronavirus(chat):
    page = requests.get('https://стопкоронавирус.рф/information/')
    soup = BeautifulSoup(page.text, "html.parser")
    found = str(soup.select('cv-stats-virus')).split(':stats-data=')
    found = str(found[1]).split(',')
    sickChange = str(found[1]).replace('"sickChange":"', '').replace('"', '')
    diedChange = str(
        found[5]).replace(
            '"diedChange":"', '').replace('"', '').replace(r'\u00a0', ' ')
    what_to_send = (
        f'Корона тайм зяблс. За сегодня в России:\n'
        f'Заболевших {sickChange} \n'
        f'Смертей {diedChange} \n'
    )
    bot.send_message(chat_id=chat, text=what_to_send)
