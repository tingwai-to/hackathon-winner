import hashlib
import json
import os
import random
import string
import traceback

import markovify
from django.conf import settings
from django.http import HttpResponseBadRequest, HttpResponse
from django.shortcuts import render
from sparkpost import SparkPost

from hackathon.models import Subscription

with open(os.path.join(settings.PROJECT_ROOT, 'markov.json'), 'r') as f:
    model_json = json.load(f)

model = markovify.Text.from_json(model_json)
sp = SparkPost(os.environ['SPARKPOST_KEY'])


def index_view(request):
    pitch = model.make_short_sentence(140)
    return render(request, 'index.html', {'pitch': pitch})


def server_error_view(request):
    print('Server Error. Printing stack trace.')
    traceback.print_exc()
    return render(request, '500.html')


def subscribe_view(request):
    email = request.POST.get('email')
    try:
        frequency = int(request.POST.get('frequency'))
        if not (0 <= frequency <= 1):
            return HttpResponseBadRequest('Invalid email frequency')
        subscription, created = Subscription.objects.update_or_create(email=email, defaults={
            'frequency': frequency,
        })
        if False and not created:
            return HttpResponseBadRequest('This subscription already exists!')
        else:
            if settings.DEBUG:
                unsub_url = "http://localhost:8000/unsubscribe?email={}".format(email)
            else:
                unsub_url = "https://hackgen.herokuapp.com/unsubscribe?email={}".format(email)
            pitch = model.make_short_sentence(140)
            sp.transmissions.send(
                use_sandbox=True,
                recipients=[email],
                html='<p>You have subscribed to HackGen! Here is the latest brilliant hackathon idea:</p><p>{}</p><a href="{}">Click here to unsubscribe</a>'.format(pitch, unsub_url),
                from_email='sandbox@sparkpostbox.com"',
                subject='Hello from HackGen'
            )
            return HttpResponse('Success!')
    except:
        traceback.print_exc()
        return HttpResponseBadRequest('Could not subscribe email address')


def unsubscribe_view(request):
    email = request.GET.get('email')
    try:
        subscription = Subscription.objects.get(email=email)
    except:
        return HttpResponse('Failed to cancel subscription')
    subscription.delete()
    if settings.DEBUG:
        unsub_url = "http://localhost:8000/unsubscribe?email={}".format(email)
    else:
        unsub_url = "https://hackgen.herokuapp.com/unsubscribe?email={}".format(email)
    sp.transmissions.send(
        use_sandbox=True,
        recipients=[email],
        html='You have successfuly unsubscribed from HackGen',
        from_email='sandbox@sparkpostbox.com"',
        subject='Hello from HackGen'
    )
    return HttpResponse('Successfuly unsubscribed!')
