from django.contrib import admin
from .models import *
from django.urls import reverse
from django.utils.html import format_html


# Register your models here.
class MatchModelAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'link_to_team1', 'link_to_team2', 'is_running', 'log_file', 'winner','date']
    list_filter = ['is_running', 'winner']

    def link_to_team1(self, obj):
        link = reverse("admin:register_team_change", args=[obj.team1.id])  # model name has to be lowercase
        return format_html("<a href='{}'>{}</a>", link, obj.team1.__str__())

    def link_to_team2(self, obj):
        link = reverse("admin:register_team_change", args=[obj.team2.id])  # model name has to be lowercase
        return format_html("<a href='{}'>{}</a>", link, obj.team2.__str__())

    link_to_team1.allow_tags = True
    link_to_team1.short_description = "Team1"
    link_to_team2.allow_tags = True
    link_to_team2.short_description = "Team2"

    class Meta:
        model = Match


admin.site.register(Match, MatchModelAdmin)


class CodeModelAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'link_to_team', 'version']
    list_filter = ['team']

    def link_to_team(self, obj):
        link = reverse("admin:register_team_change", args=[obj.team.id])  # model name has to be lowercase
        return format_html("<a href='{}'>{}</a>", link, obj.team.__str__())

    link_to_team.allow_tags = True
    link_to_team.short_description = 'Team'

    class Meta:
        model = Code


admin.site.register(Code, CodeModelAdmin)
