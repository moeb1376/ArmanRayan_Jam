from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Competition(models.Model):
    competition_name = models.CharField(max_length=200, verbose_name=_("Name"))
    competition_level = models.IntegerField(verbose_name=_("Level"))

    def __str__(self):
        return self.competition_name

    class Meta:
        ordering = ['competition_level']
        verbose_name = _("Competition")
        verbose_name_plural = _("Competitions")


class Grade(models.Model):
    grade_name = models.CharField(max_length=200, verbose_name=_("Name"))

    def __str__(self):
        return self.grade_name

    class Meta:
        ordering = ['grade_name']
        verbose_name = _("Grade")
        verbose_name_plural = _("Grades")


class University(models.Model):
    university_name = models.CharField(max_length=200, verbose_name=_("Name"))
    university_city = models.CharField(max_length=200, verbose_name=_("City"))

    def __str__(self):
        return self.university_name

    class Meta:
        ordering = ['university_name']
        verbose_name = _("University")
        verbose_name_plural = _("Universities")


class Language(models.Model):
    language_name = models.CharField(max_length=200, verbose_name=_("Name"))

    def __str__(self):
        return self.language_name

    class Meta:
        ordering = ['language_name']
        verbose_name = _("Language")
        verbose_name_plural = _("Languages")


class Mentor(models.Model):
    first_name = models.CharField(max_length=200, verbose_name=_("First name"))
    last_name = models.CharField(max_length=200, verbose_name=_("Last name"))
    code = models.CharField(max_length=6, verbose_name=_("Code"))
    university = models.ForeignKey(University, on_delete=models.CASCADE, verbose_name=_("University"))

    class Meta:
        ordering = ["university__university_name", "first_name"]
        verbose_name = _("Mentor")
        verbose_name_plural = _("Mentors")

    def __str__(self):
        return self.first_name + ' ' + self.last_name + '|' + self.university.university_name
