from django.urls import path,re_path
from django.conf.urls import url
from .views import *

app_name = 'setting'
urlpatterns = [
    # path('setting/', setting_page, name='setting'),
    re_path(r'setting(?P<active_member>\d*)/', setting_page, name='setting'),
    path('old_setting/', setting_page, name='old_setting'),
    url(r'^mentor_ajax/$', mentor_ajax, name='mentor_ajax'),

    # path('test_ajax',test_ajax,name='test_ajax'),s
]
