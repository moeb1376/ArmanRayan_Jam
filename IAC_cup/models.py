import datetime

from django.db import models
from django.utils import timezone
from main.models import Competition
from register.models import Team, auth_user
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _


class Cup(models.Model):
    name = models.CharField(max_length=20, verbose_name=_("Name"))
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name="competition",
                                    verbose_name=_("Competition"))
    start_date = models.DateTimeField(default=now, verbose_name=_("Start Date"))
    end_date = models.DateTimeField(verbose_name=_("End Date"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("IAC Cup")
        verbose_name_plural = _("IAC Cups")
        ordering = ["competition__competition_level", "start_date"]


class Key(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="Team", verbose_name=_("Team"))
    cup = models.ForeignKey(Cup, on_delete=models.CASCADE, related_name="Cup", verbose_name=_("Cup"))
    key = models.CharField(max_length=25, unique=True, blank=True, verbose_name=_("Key"))
    password_used = models.BooleanField(default=False, verbose_name=_("Password Used"))
    last_connection = models.DateTimeField(default=now, verbose_name=_("Last Connection"))

    def __str__(self):
        return self.team.user_team.username + " | " + self.cup.name

    class Meta:
        verbose_name_plural = _("Keys")
        verbose_name = _("Key")
        ordering = ['cup']


class DatasetCup(models.Model):
    data = models.CharField(max_length=200, null=False, blank=False, verbose_name=_("Data"))
    cup = models.ForeignKey(Cup, on_delete=models.CASCADE, verbose_name=_("Cup"))
    answer = models.CharField(max_length=200, null=False, blank=False, verbose_name=_("Answer"))

    def __str__(self):
        return self.data + " | " + self.cup.name

    class Meta:
        verbose_name = _("Dataset IAC Cup")
        verbose_name_plural = _("Dataset IAC Cups")
        ordering = ['cup']


class UsersAnswer(models.Model):
    data = models.ForeignKey(DatasetCup, on_delete=models.CASCADE, verbose_name=_("Data"))
    user = models.ForeignKey(Team, on_delete=models.CASCADE, verbose_name=_("User"))
    user_answer = models.CharField(max_length=200, null=False, blank=False, verbose_name=_("User Answer"))
    time_send = models.DateTimeField(verbose_name=_("Time Send"))
    time_receive = models.DateTimeField(null=True, blank=True, verbose_name=_("Time Receive"))

    def __str__(self):
        return self.data.data + "|" + self.user.user_team.username

    class Meta:
        verbose_name = _("User Answer")
        verbose_name_plural = _("User Answers")
        ordering = ['data__cup']
