from django.conf.urls import url
from django.urls import path
from django.views.generic import RedirectView

from .views import *

app_name = 'register'
urlpatterns = [
    path('register', register_page2, name='register'),
    path('login', login_page2, name='login'),
    path('', RedirectView.as_view(url='/login')),

]
