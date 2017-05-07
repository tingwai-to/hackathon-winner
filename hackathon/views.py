import traceback

from django.http import HttpResponse
from django.shortcuts import render
from sklearn.externals import joblib

from hackathon.models import Project

model = joblib.load('model.pkl')


def index_view(request):
    return render(request, 'index.html')


def predict_view(request):
    text = request.GET.get('text').encode('ascii', 'ignore').strip()
    return HttpResponse(model.predict_proba([text])[0][1])


def projects_view(request):
    projects = Project.objects.all()[:40]
    return render(request, 'projects.html', {'projects': projects})


def server_error_view(request):
    print('Server Error. Printing stack trace.')
    traceback.print_exc()
    return render(request, '500.html')
