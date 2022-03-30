#!/bin/bash
cd telegram_chupakabrada_bot
source venv/bin/activate
python3 -c 'from today_corona import *; from conf import home_telega; coronavirus(home_telega)'