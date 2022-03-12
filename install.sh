#!/bin/bash
killall screen
rm -rf /root/telegram_chupakabrada_bot
cd /root/ && git clone https://github.com/feel2code/telegram_chupakabrada_bot
cp /root/conf.py /root/telegram_chupakabrada_bot/conf.py
# removing starting script if exists
if [[ -e install.sh ]]
then
rm -rf /root/install.sh
fi
# copying starting script loaded from github
cp /root/telegram_chupakabrada_bot/start.sh /root/start.sh
chmod +x /root/start.sh
apt install python3-venv -yy
cd telegram_chupakabrada_bot
python3 -m venv venv
source venv/bin/activate
pip install -r /root/telegram_chupakabrada_bot/requirements.txt
screen -dm python3 /root/telegram_chupakabrada_bot/bot.py
sleep 3
screen -dm python3 /root/telegram_chupakabrada_bot/exchange.py
