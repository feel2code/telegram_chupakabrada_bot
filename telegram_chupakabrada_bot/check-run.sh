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

	exchange=$(pgrep -fc 'python exchange.py')
	if [ "$exchange" -eq 0 ]
then {
	echo "Running exchange.py"
        sleep 1
    source venv/bin/activate
	  python exchange.py &
}
else 
{
	echo "Exchange already running!"
}
fi
sleep 30
done