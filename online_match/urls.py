from django.conf.urls import url
from django.urls import path
from django.views.generic import RedirectView

from .views import *

app_name = 'online_match'
urlpatterns = [
    path('playKhodam', online_match, name='online_match'),
    path('loginse', test, name='login_se'),
    url(r'^play_online_ajax/$', play_online_ajax, name='play_online_ajax'),
    url(r'^file_upload_ajax/$', upload_view, name='file_upload_ajax'),

]
