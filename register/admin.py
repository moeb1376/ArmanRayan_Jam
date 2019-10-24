from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _

from .models import *


class TeamModelAdmin(admin.ModelAdmin):
    list_display = ['user_team', 'get_email', 'competition', 'university', 'language']
    list_filter = ['user_team__last_login']

    def get_email(self, obj):
        return obj.user_team.email

    get_email.allow_tags = True
    get_email.short_description = _('Email')

    class Meta:
        model = Team


class MyUserModelAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'email', 'link_to_team', 'is_head', 'university', 'grade', 'competition_level',
                    'entrance_year_show']
    list_filter = ['university', 'team__competition__competition_name', 'grade','is_head','entrance_year']

    def entrance_year_show(self, obj):
        return obj.get_normal_entrance_year()

    def link_to_team(self, obj):
        link = reverse("admin:register_team_change", args=[obj.team.id])  # model name has to be lowercase
        return format_html("<a href='{}'>{}</a>", link, obj.team.__str__())

    def competition_level(self, obj):
        return obj.team.competition.competition_name

    link_to_team.allow_tags = True
    link_to_team.short_description = _('Team')
    competition_level.allow_tags = True
    competition_level.short_description = _('Competition')
    entrance_year_show.allow_tags = True
    entrance_year_show.short_description = _('Entrance_year')

    class Meta:
        model = MyUser


admin.site.register(Team, TeamModelAdmin)
admin.site.register(MyUser, MyUserModelAdmin)
