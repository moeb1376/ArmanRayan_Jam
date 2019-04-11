import datetime

from django.db import models
from django.utils import timezone
from main.models import Competition
from register.models import Team, auth_user


# Create your models here.

class Cup(models.Model):
    name = models.CharField(max_length=20)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name="competition")
    start_date = models.DateTimeField(default=timezone.now())
    end_date = models.DateTimeField()

    def __str__(self):
        return self.name


class Key(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="Team")
    cup = models.ForeignKey(Cup, on_delete=models.CASCADE, related_name="Cup")
    key = models.CharField(max_length=25, unique=True)
    password_used = models.BooleanField(default=False)
    last_connection = models.DateTimeField(default=timezone.now())


class TestOneToOne(models.Model):
    id_team = models.OneToOneField(auth_user, on_delete=models.CASCADE, primary_key=True)
    cup = models.OneToOneField(Cup, on_delete=models.CASCADE)
