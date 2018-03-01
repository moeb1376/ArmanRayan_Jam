from django.contrib.auth import views as auth_view
from django.urls import path, include, re_path
from django.views.generic import TemplateView, RedirectView
from .views import *

app_name = 'main'
urlpatterns = [
    # path('index', TemplateView.as_view(template_name='main/index.html')),
    path('update', TemplateView.as_view(template_name='main/start.html')),
    path('play', RedirectView.as_view(url='/update')),
    path('play_iac', RedirectView.as_view(url='/update')),
    path('cup', RedirectView.as_view(url='/update')),
    path('cup_iac', RedirectView.as_view(url='/update')),

]
