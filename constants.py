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
