#!/bin/bash
killall screen
rm -rf /root/tele*
cd /root/ && git clone https://github.com/feel2code/telegram_chupakabrada_bot
cp /root/conf.py /root/telegram_chupakabrada_bot/conf.py
screen -dm python3 /root/telegram_chupakabrada_bot/bot.py
