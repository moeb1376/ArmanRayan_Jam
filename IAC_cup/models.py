import datetime

from django.db import models
from django.utils import timezone
from main.models import Competition
from register.models import Team, auth_user
from django.utils.timezone import now


# Create your models here.

class Cup(models.Model):
    name = models.CharField(max_length=20)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name="competition")
    start_date = models.DateTimeField(default=now)
    end_date = models.DateTimeField()

    def __str__(self):
        return self.name


class Key(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="Team")
    cup = models.ForeignKey(Cup, on_delete=models.CASCADE, related_name="Cup")
    key = models.CharField(max_length=25, unique=True, blank=True)
    password_used = models.BooleanField(default=False)
    last_connection = models.DateTimeField(default=now)

    def __str__(self):
        return self.team.user_team.username + " | " + self.cup.name


class DatasetCup(models.Model):
    data = models.CharField(max_length=200, null=False, blank=False)
    cup = models.ForeignKey(Cup, on_delete=models.CASCADE)
    answer = models.CharField(max_length=200, null=False, blank=False)

    def __str__(self):
        return self.data + " | " + self.cup.name


class UsersAnswer(models.Model):
    data = models.ForeignKey(DatasetCup, on_delete=models.CASCADE)
    user = models.ForeignKey(Team, on_delete=models.CASCADE)
    user_answer = models.CharField(max_length=200, null=False, blank=False)
    time_send = models.DateTimeField()
    time_receive = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.data.data + "|" + self.user.user_team.username