import json

import markovify

with open('markov.txt', 'r') as f:
    corpus = f.read()

text_model = markovify.Text(corpus, state_size=3)
model = text_model.to_json()

with open('model.json', 'w') as f:
    json.dump(model, f)

