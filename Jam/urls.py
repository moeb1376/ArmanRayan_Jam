"""Jam URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import password_reset, password_reset_done, password_reset_confirm, \
    password_reset_complete, PasswordResetView
from dbbackup_ui.views import BackupView

urlpatterns = [
    path('auth/admin/superuser/', admin.site.urls),
    # url(r'^auth/admin/superuser/backups/', include('dbbackup_ui.urls')),
    path('auth/admin/superuser/backup', BackupView.as_view(), name='backup_view'),
    path('', include('main.urls')),
    path('', include('register.urls')),
    path('', include('SPC_main.urls')),
    # path('', include('team_setting.urls')),
    path('', include('setting.urls')),
    path('', include('online_match.urls')),
    path('reset-password', password_reset, name='reset_password'),
    path('reset-password/done', password_reset_done, name='password_reset_done'),
    url(r'^reset-password/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        password_reset_confirm, name='password_reset_confirm'),
    path('reset-password/complete', password_reset_complete, name='password_reset_complete'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
