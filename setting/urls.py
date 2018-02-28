from django.urls import path
from .views import *

app_name = 'setting'
urlpatterns = [
    path('setting', setting_page, name='setting'),
    path('testchange', test_change, name='setting'),
    path('test_image_field',test_image_field,name='test_image_field')
]
