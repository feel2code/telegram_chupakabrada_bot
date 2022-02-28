#!/bin/bash
killall screen
rm -rf /root/tele*
cd /root/ && git clone https://github.com/feel2code/telegram_chupakabrada_bot
cp /root/conf.py /root/telegram_chupakabrada_bot/conf.py
# removing starting script if exists
if [[ -e start.sh ]]
then
rm -rf /root/start.sh
fi
# copying starting script loaded from github
cp /root/telegram_chupakabrada_bot/start.sh /root/start.sh
chmod +x /root/start.sh
pip install -r /root/telegram_chupakabrada_bot/requirements.txt
screen -dm python3 /root/telegram_chupakabrada_bot/bot.py
sleep 2
screen -dm python3 /root/telegram_chupakabrada_bot/exchange.py
