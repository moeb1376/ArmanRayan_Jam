from django.urls import path
from django.conf.urls import url
from .views import *

app_name = 'setting'
urlpatterns = [
    path('setting', setting_page, name='setting'),
    path('testchange', test_change, name='testchange'),
    url(r'^test_ajax/$',test_ajax,name='test_ajaxs'),
    # path('test_ajax',test_ajax,name='test_ajax'),
    path('test_image_field',test_image_field,name='test_image_field')
]
