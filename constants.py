from conf import key_for_stats
from films import films_command
from weather_module import add_city, delete_city, weather_in_city
from holiday import holiday
from selects import sticker_send
from stats import send_statistics
from today_corona import coronavirus
from weather_module import (
    weather_in_city, add_city, delete_city, get_weather_list)


TEMPERATURE_NOT_EXIST = '999'

GODZILLA = '3 4 5 0 D'

ZOO_DICT = {
    '/хрю': 'pig_stickers',
    '/гав': 'dog_stickers',
}

SELECTS = {
    '/about': 'SELECT about_text FROM about where about_id=1',
    '/about@chupakabrada_bot': 'SELECT about_text FROM about where about_id=1',
    '/quote': 'select quote from quotes order by random() limit 1',
    '/quote@chupakabrada_bot': (
        'select quote from quotes order by random() limit 1'),
    '/start': 'SELECT start_text FROM start_q where start_id=1',
    '/start@chupakabrada_bot': (
        'SELECT start_text FROM start_q where start_id=1'),
}

COMMANDS_QUERY = {
    '/add': 123,
    '/add@chupakabrada_bot': 123,
    '/delete': 124,
    '/delete@chupakabrada_bot': 124,
    '/weather': 125,
    '/weather@chupakabrada_bot': 125,
}

COMMANDS_DO = {
    '/add': add_city,
    '/add@chupakabrada_bot': add_city,
    '/delete': delete_city,
    '/delete@chupakabrada_bot': delete_city,
    '/weather': weather_in_city,
    '/weather@chupakabrada_bot': weather_in_city,
    '/top_cinema': films_command,
    '/top_cinema@chupakabrada_bot': films_command,
}

COMMANDS_FUNCS = {
    key_for_stats: send_statistics,
    '/weather_list': get_weather_list,
    '/weather_list@chupakabrada_bot': get_weather_list,
    '/holiday': holiday,
    '/holiday@chupakabrada_bot': holiday,
    '/corona': coronavirus,
    '/corona@chupakabrada_bot': coronavirus,
    '/sticker': sticker_send,
    '/sticker@chupakabrada_bot': sticker_send,
}
