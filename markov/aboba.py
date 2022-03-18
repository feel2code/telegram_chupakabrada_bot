import markovify


def markov(message):
    markov_text = open('markov/markov.txt', "a")
    markov_text.write(f'{message.text}. ')
    markov_text.close()
    text = open('markov/markov.txt', encoding='utf8').read()
    text_model = markovify.Text(text, state_size=3)
    for i in range(1):
        return text_model.make_sentence(tries=50)
