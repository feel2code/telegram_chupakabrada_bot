from bs4 import BeautifulSoup

output = ''
for page in range(1, 4):
    HTMLFile = open(f'messages{page}.html', "r")
    index = HTMLFile.read()
    soup = BeautifulSoup(index, "html.parser")
    datas = soup.find_all('div', class_='text')
    for data in datas:
        data_text = str(
            data.text
            ).replace(
                '       ', ''
            ).replace(
                '\n', ''
            )
        if 'http' in data_text:
            pass
        else:
            output += f'{data_text}. '

output = output.replace('HOME TELEGA CREW stonks 2.0      . ', '')
f = open("markov.txt", "w")
f.write(output)
f.close()