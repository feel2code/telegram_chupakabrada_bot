#!/bin/bash
while true
do
	bot=$(ps aux | grep 'python3 /root/telegram_chupakabrada_bot/bot.py' | wc -l)
	if [ "$bot" -eq 1 ]
then {
	echo "Running chupakabra bot"
        sleep 1
    cd /root/telegram_chupakabrada_bot
    source venv/bin/activate
	python3 /root/telegram_chupakabrada_bot/bot.py &
}
else 
{
	echo "Bot already running!"
}
fi

	exchange=$(ps aux | grep 'python3 /root/telegram_chupakabrada_bot/exchange.py' | wc -l)
	if [ "$exchange" -eq 1 ]
then {
	echo "Running exchange.py"
        sleep 1
    cd /root/telegram_chupakabrada_bot
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