from django.conf.urls import url
from django.urls import path
from django.views.generic import RedirectView

from .views import *

urlpatterns = [
    path('play', online_match, name='online_match'),
    path('new_play', online_match, name='new_online_match'),
    path('log', log_view, name='log'),
    path('new_log', log_view, name='new_log'),
    url(r'^play_online_ajax/$', play_online_ajax, name='play_online_ajax'),
    url(r'^file_upload_ajax/$', upload_view, name='file_upload_ajax'),
]
app_name = 'online_match'
