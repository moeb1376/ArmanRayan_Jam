from django.conf.urls import url
from django.urls import path
from django.views.generic import TemplateView
from .views import *

app_name = 'SPC_main'
urlpatterns = [
    path('jaam', SPC_main_page, name='SPC_main_page'),
    path('logout', team_logout, name='logout'),
    path('table', table_view, name='table-spc'),
    path('cup', cup_view, name='cup-view'),
    url(r'^add_team_ajax/$', add_team_to_cup, name='file_upload_ajax'),
]
