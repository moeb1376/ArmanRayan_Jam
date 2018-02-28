from django.contrib.auth import views as auth_view
from django.urls import path, include
from django.views.generic import TemplateView
from .views import *

app_name = 'main'
urlpatterns = [
    # path('index', TemplateView.as_view(template_name='main/index.html')),
]
