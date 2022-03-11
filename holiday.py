import requests
from bs4 import BeautifulSoup
from datetime import datetime

from connections import bot, cur


def holiday(chat_id):
    day = datetime.now().day
    month = datetime.now().month

    cur.execute("SELECT month_name FROM months where id=" + str(month) + "; ")
    fetched_month_name = str(
        cur.fetchall()).replace("[('", "").replace("',)]", "")
    data = str(day) + '_' + fetched_month_name
    today = []
    page = requests.get(
        'https://ru.wikipedia.org/wiki/' + 'Категория:Праздники_' + data)
    soup = BeautifulSoup(page.text, "html.parser")
    for item in soup.select("li"):
        today.append(item.get_text())
    try:
        index = today.index('Праздники' + data.replace(str(day) + '_', ' '))
        i = index
        while len(today) != i:
            today.pop(index)
        today[0] = ' ' + today[0]
        case = str([word + '\n' for word in today]).replace(
            ',', '').replace('[', '').replace(']', '').replace(
            '[', '').replace("'", "").replace(r"\n", "\n")
        bot.send_message(chat_id=chat_id, text=(
            'Сиводня ' + str(datetime.now().date()) + ': \n' + case))
    except ValueError:
        bot.send_message(chat_id=chat_id, text=(
            'Сиводня ' + str(datetime.now().date()) + ' праздников нет.'))
