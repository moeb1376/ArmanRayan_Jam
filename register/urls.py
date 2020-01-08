from django.urls import path

from django.views.generic import RedirectView

from .views import *

app_name = 'register'
urlpatterns = [
    path('register/', register_page, name='register'),
    path('old_register/', old_register_page, name='old_register'),
    path('login/', login_page, name='login'),
    path('old_login/', old_login_page, name='old_login'),
    path('', RedirectView.as_view(url='/login')),

]
