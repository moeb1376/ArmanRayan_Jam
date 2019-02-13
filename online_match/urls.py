from django.conf.urls import url
from django.urls import path
from django.views.generic import RedirectView

from .views import *

urlpatterns = [
    path('old_play/', online_match, name='old_online_match'),
    path('play/', online_match, name='online_match'),
    path('old_log/', log_view, name='old_log'),
    path('log/', log_view, name='log'),
    url(r'^play_online_ajax/$', play_online_ajax, name='play_online_ajax'),
    url(r'^file_upload_ajax/$', upload_view, name='file_upload_ajax'),
]
app_name = 'online_match'
