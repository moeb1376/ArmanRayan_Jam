from django.urls import path

from django.views.generic import RedirectView

from .views import *

app_name = 'IAC_cup'
urlpatterns = [
    path('iac_cup/', render_page, name='render_page'),
    path("api/get-key", get_key, name="get-key"),
    path("api/connect", connect, name="connection"),
    path("api/get-data", get_data, name="get-data"),
]
