from django.urls import path

from django.views.generic import RedirectView

from .views import login_page2, register_page2, new_login, new_register_page

app_name = 'register'
urlpatterns = [
    path('register', new_register_page, name='register'),
    # path('new_register', new_register_page, name='new_register'),
    path('login', new_login, name='login'),
    # path('new_login', new_login, name='new_login'),
    path('', RedirectView.as_view(url='/login')),

]
