from django.urls import path
from django.views.generic import TemplateView
from .views import *

app_name = 'main'
urlpatterns = [
    path('', TemplateView.as_view(template_name='main/index.html')),
]
