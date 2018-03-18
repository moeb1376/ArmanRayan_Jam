from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import *


class TeamModelAdmin(admin.ModelAdmin):
    list_display = ['user_team', 'competition', 'university', 'language']

    class Meta:
        model = Team


class MyUserModelAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'link_to_team', 'is_head', 'university', 'get_normal_entrance_year']
    list_filter = ['university']

    def link_to_team(self, obj):
        link = reverse("admin:register_team_change", args=[obj.team.id])  # model name has to be lowercase
        return format_html("<a href='{}'>{}</a>", link, obj.team.__str__())

    link_to_team.allow_tags = True

    class Meta:
        model = MyUser


# Register your models here.
admin.site.register([Test])
admin.site.register(Team, TeamModelAdmin)
admin.site.register(MyUser, MyUserModelAdmin)
