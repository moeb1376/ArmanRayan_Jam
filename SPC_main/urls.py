from django.urls import path
from django.views.generic import TemplateView
from .views import *

app_name = 'SPC_main'
urlpatterns = [
    path('jaam', SPC_main_page, name='SPC_main_page'),
    path('logout', team_logout, name='logout'),
    path('table', table_view, name='table-spc'),
]
