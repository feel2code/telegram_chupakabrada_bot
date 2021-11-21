import time
import telebot
from conf import *
import random
from sys import argv

script, chat = argv
bot = telebot.TeleBot(name)
time.sleep(random.randint(1, 28800))
bot.send_message(chat_id=chat, text="Ну шооо, как дела у вас тут, палучаица, м?")
