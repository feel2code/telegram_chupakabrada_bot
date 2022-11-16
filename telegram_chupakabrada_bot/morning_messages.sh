#!/bin/bash
cd ~/telegram_chupakabrada_bot || exit
source venv/bin/activate
python3 weather_module.py
sleep 2
python3 holiday.py
