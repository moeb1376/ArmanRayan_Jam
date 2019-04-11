import datetime

from django.db import models
from django.utils import timezone
from main.models import Competition
from register.models import Team


# Create your models here.

class Cup(models.Model):
    name = models.CharField(max_length=20)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name="competition")
    start_date = models.DateField(default=timezone.now())
    end_date = models.DateField()


class Key(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="Team")
    cup = models.ForeignKey(Cup, on_delete=models.CASCADE, related_name="Cup")
    key = models.CharField(max_length=25, unique=True)
    password_used = models.BooleanField()
