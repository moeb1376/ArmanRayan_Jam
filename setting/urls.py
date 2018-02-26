from django.urls import path
from .views import *

app_name = 'setting'
urlpatterns = [
    path('setting', setting_page, name='setting'),
]
