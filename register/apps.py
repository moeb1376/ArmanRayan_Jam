from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class RegisterConfig(AppConfig):
    name = 'register'
    verbose_name = _("Register")
