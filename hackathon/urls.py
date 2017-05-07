from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse

from hackathon import views

admin.autodiscover()

handler500 = 'hackathon.views.server_error_view'
urlpatterns = [
    url(r'^$', views.index_view, name='home'),
    url(r'^projects/$', views.projects_view, name='projects'),
    url(r'^predict/', views.predict_view, name='predict'),
]
