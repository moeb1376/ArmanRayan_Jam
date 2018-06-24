from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Cup


# Register your models here.

class CupModelAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'link_to_team', 'competition', 'cup_number']
    list_filter = ['team', 'cup_number']

    def link_to_team(self, obj):
        link = reverse("admin:register_team_change", args=[obj.team.id])  # model name has to be lowercase
        return format_html("<a href='{}'>{}</a>", link, obj.team.__str__())

    link_to_team.allow_tags = True
    link_to_team.short_description = 'Team'

    class Meta:
        model = Cup


admin.site.register(Cup,CupModelAdmin)
