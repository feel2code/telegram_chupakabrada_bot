#!/bin/bash
apt-get install postgresql-12 -yy
mv /etc/postgresql/12/main/pg_hba.conf /etc/postgresql/12/main/pg_hba.conf.bak
cp misc/pg_hba.conf /etc/postgresql/12/main/pg_hba.conf
# copying secret conf file from root directory
cp /root/conf.py /root/telegram_chupakabrada_bot/conf.py
cd /root/telegram_chupakabrada_bot || exit
chmod +x install.sh
chmod +x morning_messages.sh
chmod +x check-run.sh
# copying starting script loaded from github
apt install python3-pip python3-venv -yy
python3 -m venv venv
source venv/bin/activate
python3 -m pip install --upgrade pip
pip install -r /root/telegram_chupakabrada_bot/requirements.txt
# run script that checking if bot and exchange apps are running
/root/telegram_chupakabrada_bot/check-run.sh &