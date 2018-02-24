from django.urls import path
from .views import *

app_name = 'register'
urlpatterns = [
    path('register', register_page2, name='register'),
    path('login', login_page2, name='login')
]
