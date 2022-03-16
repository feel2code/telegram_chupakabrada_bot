#!/bin/bash
killall python3
rm -rf /root/telegram_chupakabrada_bot
cd /root/ && git clone https://github.com/feel2code/telegram_chupakabrada_bot
# copying secret conf file from root directory
cp /root/conf.py /root/telegram_chupakabrada_bot/conf.py
cd /root/telegram_chupakabrada_bot
chmod +x install.sh
chmod +x morning_messages.sh
chmod +x check-run.sh
# copying starting script loaded from github
apt install python3-venv -yy
python3 -m venv venv
source venv/bin/activate
pip install -r /root/telegram_chupakabrada_bot/requirements.txt
python3 /root/telegram_chupakabrada_bot/bot.py &
sleep 3
python3 /root/telegram_chupakabrada_bot/exchange.py &
sleep 3
# run script that checking if bot and exchange apps are running
/root/telegram_chupakabrada_bot/check-run.sh &