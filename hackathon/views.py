import json
import os
import traceback

import markovify
from django.conf import settings
from django.shortcuts import render

with open(os.path.join(settings.PROJECT_ROOT, 'markov.json'), 'r') as f:
    model_json = json.load(f)

model = markovify.Text.from_json(model_json)


def index_view(request):
    pitch = model.make_short_sentence(140)
    return render(request, 'index.html', {'pitch': pitch})


def server_error_view(request):
    print('Server Error. Printing stack trace.')
    traceback.print_exc()
    return render(request, '500.html')
