import json
import os

from django.conf import settings
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        texts = []

        project_dir = os.path.join(settings.PROJECT_ROOT, '..', 'projects')
        for fname in os.listdir(project_dir):
            path = os.path.join(project_dir, fname)
            with open(path, 'r') as json_file:
                js = json.load(json_file)

            text = js['pitch'].strip()
            if js['is_winner']:
                texts.append(text)

        with open(os.path.join(settings.PROJECT_ROOT, 'corpus.txt'), 'w') as f:
            f.write('\n'.join(texts))
