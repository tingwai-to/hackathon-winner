from __future__ import print_function

import json
import os

import markovify
from django.conf import settings
from django.core.management import BaseCommand

from hackathon.models import Subscription

from sparkpost import SparkPost

with open(os.path.join(settings.PROJECT_ROOT, 'markov.json'), 'r') as f:
    model_json = json.load(f)

model = markovify.Text.from_json(model_json)
sp = SparkPost(os.environ['SPARKPOST_KEY'])


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('frequency', type=int)

    def handle(self, *args, **options):
        frequency = options['frequency']
        assert 0 <= frequency <= 1
        subscriptions = Subscription.objects.filter(frequency=frequency)
        for sub in subscriptions:
            email = sub.email
            print('emailing', email)
            pitch = model.make_short_sentence(140)
            if settings.DEBUG:
                unsub_url = "http://localhost:8000/unsubscribe?email={}".format(email)
            else:
                unsub_url = "https://hackgen.herokuapp.com/unsubscribe?email={}".format(email)

            sp.transmissions.send(
                use_sandbox=True,
                recipients=[email],
                html='<p>{}</p><a href="{}">Unsubscribe</a>'.format(pitch, unsub_url),
                from_email='sandbox@sparkpostbox.com"',
                subject='The latest brilliant hackathon idea from HackGen'
            )
