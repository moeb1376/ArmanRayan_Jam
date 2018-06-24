from django.conf.urls import url
from django.urls import path
from django.views.generic import RedirectView

from .views import *

app_name = 'online_match'
urlpatterns = [
    path('play', online_match, name='online_match'),
    path('log', log_view, name='log'),
    path('loginse', test, name='login_se'),
    path('online_match_result', online_match_result, name='test-bash-json'),
    url(r'^play_online_ajax/$', play_online_ajax, name='play_online_ajax'),
    url(r'^file_upload_ajax/$', upload_view, name='file_upload_ajax'),

]
