#!/bin/bash
# please add here path instead of /home
path=/home
cd $path
source venv/bin/activate
python weather_module.py
sleep 2
python holiday.py
