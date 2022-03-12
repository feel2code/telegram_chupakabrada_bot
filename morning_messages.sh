#!/bin/bash
cd telegram_chupakabrada_bot
source venv/bin/activate
python3 -c 'from weather_module import *; from conf import home_telega; get_weather_list(home_telega)'
sleep 2
python3 -c 'from holiday import *; from conf import home_telega; holiday(home_telega)'
