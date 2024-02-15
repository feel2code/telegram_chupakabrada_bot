#!/bin/bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

crontab misc/crontab.txt

mkdir misc/voices && mv misc/voices.tar.xz misc/voices/voices.tar.xz
cd misc/voices
tar -xvf voices.tar.xz
cd ..

cp tel_bot.service /etc/systemd/system/tel_bot.service
systemctl enable tel_bot.service
systemctl start tel_bot.service
systemctl daemon-reload

