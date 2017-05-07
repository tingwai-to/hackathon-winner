import json
import os

texts = []

project_dir = 'projects'
for fname in os.listdir(project_dir):
    path = os.path.join(project_dir, fname)
    with open(path, 'r') as json_file:
        js = json.load(json_file)

    text = js['pitch'].strip()
    if js['is_winner']:
        texts.append(text)

with open('markov.txt', 'w') as f:
    f.write('\n'.join(texts))
