import json
import os

import markovify
from django.conf import settings
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open(os.path.join(settings.PROJECT_ROOT, 'corpus.txt'), 'r') as f:
            corpus = f.read()

        text_model = markovify.Text(corpus, state_size=3)
        model = text_model.to_json()

        with open(os.path.join(settings.PROJECT_ROOT, 'markov.json'), 'w') as f:
            json.dump(model, f)
