#!/bin/bash
while true
do
	bot=$(pgrep -fc 'python bot.py')
	if [ "$bot" -eq 0 ]
then {
	echo "Running bot.py"
        sleep 1
    source venv/bin/activate
	  python bot.py &
}
else 
{
	echo "Bot already running!"
}
fi

sleep 30
done
