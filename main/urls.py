from django.contrib.auth import views as auth_view
from django.urls import path
from django.views.generic import TemplateView, RedirectView
from .views import *

app_name = 'main'
urlpatterns = [
    path('update', TemplateView.as_view(template_name='main/start.html')),
    path('update_iac', TemplateView.as_view(template_name='main/start2.html')),
    path('play_iac', RedirectView.as_view(url='/play')),
    path('table_iac', RedirectView.as_view(url='/table')),
    path('cup_iac', RedirectView.as_view(url='/cup')),
]
