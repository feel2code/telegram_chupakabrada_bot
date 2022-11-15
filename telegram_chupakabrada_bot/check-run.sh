#!/bin/bash
while true
do
	bot=$(pgrep -fc 'python3 /root/telegram_chupakabrada_bot/bot.py')
	if [ "$bot" -eq 0 ]
then {
	echo "Running bot.py"
        sleep 1
    cd /root/telegram_chupakabrada_bot || exit
    source venv/bin/activate
	python3 /root/telegram_chupakabrada_bot/bot.py &
}
else 
{
	echo "Bot already running!"
}
fi

	exchange=$(pgrep -fc 'python3 /root/telegram_chupakabrada_bot/exchange.py')
	if [ "$exchange" -eq 0 ]
then {
	echo "Running exchange.py"
        sleep 1
    cd /root/telegram_chupakabrada_bot || exit
    source venv/bin/activate
	python3 /root/telegram_chupakabrada_bot/exchange.py &
}
else 
{
	echo "Exchange already running!"
}
fi
sleep 30
done