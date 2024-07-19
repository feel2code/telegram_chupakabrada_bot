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

tar -xvf db_data.tar.gz
cp db_data.sql ..
cp db_ddl.sql ..
cd ..
DB_NAME=$(read DB_NAME_RAW < .env && echo $DB_NAME_RAW | cut -d "=" -f 2)
cp /temp/telegram_chupakabrada_bot_temp.db $DB_NAME.db
if [ ! -f $DB_NAME.db ]; then
    echo "Database not found! Creating database..."
    sqlite3 $DB_NAME.db < db_ddl.sql
    sqlite3 $DB_NAME.db < db_data.sql
else
  echo "Database already exists!"
fi

rm db_data.sql
rm db_ddl.sql
rm misc/db_data.sql

echo "Deployed!"
