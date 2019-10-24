from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import *


class UniversityAdmin(ModelAdmin):
    class Meta:
        model = University

    list_display = ['__str__', 'university_name', 'university_city']


class CompetitionAdmin(ModelAdmin):
    class Meta:
        model = Competition

    list_display = ['__str__', 'competition_name', 'competition_level']


class GradeAdmin(ModelAdmin):
    class Meta:
        model = Grade

    list_display = ['__str__', 'grade_name', ]


class LanguageAdmin(ModelAdmin):
    class Meta:
        model = Language

    list_display = ['__str__', 'language_name']


# Register your models here.
admin.site.register(University, UniversityAdmin)
admin.site.register(Competition, CompetitionAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(Grade, GradeAdmin)
admin.site.register(Mentor)
