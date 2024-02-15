#!/bin/bash
path=/root/telegram_chupakabrada_bot/telegram_chupakabrada_bot
cd $path
source venv/bin/activate
python weather_module.py
sleep 2
python holiday.py
