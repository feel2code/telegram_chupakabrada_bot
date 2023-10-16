import os

import requests
from bs4 import BeautifulSoup

from connections import bot


def coronavirus(message):
    if not isinstance(message, str):
        chat_id = message.chat.id
    else:
        chat_id = message
    soup = BeautifulSoup(
        requests.get(
            'https://стопкоронавирус.рф/information/',
            timeout=60
        ).text,
        "html.parser"
    )
    found = str(str(soup.select('cv-stats-virus')).split(':stats-data=')[1]
                ).split(',')
    sick_change = str(found[1]).replace('"sickChange":"', ''
                                        ).replace('"', '')
    died_change = str(found[5]).replace('"diedChange":"', ''
                                        ).replace('"', '').replace(r'\u00a0', ' ')
    what_to_send = ('Корона тайм, зяблс. За сегодня в России:\n'
                    f'Заболевших {sick_change} \nСмертей {died_change} \n')
    bot.send_message(chat_id=chat_id, text=what_to_send)


if __name__ == '__main__':
    coronavirus(os.getenv('HOME_TELEGA'))
