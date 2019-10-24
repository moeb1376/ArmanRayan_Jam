from django.contrib import admin
from .models import *
from django.utils.translation import ugettext_lazy as _


# Register your models here.
class CupModelAdmin(admin.ModelAdmin):
    class Meta:
        model = Cup

    list_display = ["name", "competition", 'start_date', 'end_date']
    list_filter = ['competition', 'start_date']


class KeyModelAdmin(admin.ModelAdmin):
    class Meta:
        model = Key

    list_display = ["__str__", "team", "cup", "password_used", "last_connection"]
    list_filter = ["cup", "password_used", "last_connection"]


class DatasetCupModelAdmin(admin.ModelAdmin):
    class Meta:
        model = DatasetCup

    list_display = ["__str__", "cup"]
    list_filter = ['cup']


class UserAnswerModelAdmin(admin.ModelAdmin):
    class Meta:
        model = UsersAnswer

    list_display = ["__str__", "user", "time_send", "time_receive"]
    list_filter = ['user']


admin.site.register(Cup, CupModelAdmin)
admin.site.register(Key, KeyModelAdmin)
admin.site.register(DatasetCup, DatasetCupModelAdmin)
admin.site.register(UsersAnswer, UserAnswerModelAdmin)
