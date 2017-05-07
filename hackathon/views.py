import traceback

from django.db.models import Count
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from sklearn.externals import joblib

from hackathon.models import Project, Technology

model = joblib.load('model.pkl')


def index_view(request):
    return render(request, 'index.html')


def predict_view(request):
    text = request.GET.get('text').encode('ascii', 'ignore').strip()
    return HttpResponse(model.predict_proba([text])[0][1])

def tech_search_view(request):
    query = request.GET.get('query').encode('ascii', 'ignore').strip()
    tech_query = Technology.objects.filter(name__icontains=query).annotate(num_projects=Count('projects')).order_by('-num_projects')[:15]
    return JsonResponse({'items': [{'text': tech.name, 'id': tech.name} for tech in tech_query]})

def projects_view(request):
    projects = Project.objects.all()[:40]
    technology = Technology.objects.annotate(num_projects=Count('projects')).order_by('-num_projects')
    return render(request, 'projects.html', {'projects': projects, 'technology': technology})

def server_error_view(request):
    print('Server Error. Printing stack trace.')
    traceback.print_exc()
    return render(request, '500.html')
