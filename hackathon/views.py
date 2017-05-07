import traceback

from django.db.models import Count, Q
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
    tag_names = request.GET.getlist('tech_tags')
    q = Q()
    for tag in tag_names:
        q &= Q(technologies=Technology.objects.get(name=tag))
    projects = Project.objects.filter(is_winner=True).filter(q)[:10]
    return render(request, 'projects.html', {'projects': projects})


def server_error_view(request):
    print('Server Error. Printing stack trace.')
    traceback.print_exc()
    return render(request, '500.html')
