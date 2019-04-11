from django.urls import path

from .views import *

from django.views.generic import RedirectView

app_name = 'register'
urlpatterns = [
    path('iac_cup/',render_page,name='render_page')
]
