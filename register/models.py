from django.db import models
from main.models import *


# Create your models here.

class Team(models.Model):
    team_name = models.CharField(max_length=200,)
    email = models.TextField()
    rating = models.IntegerField()
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    code_address = models.TextField()
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    password = models.CharField(max_length=200)
    win = models.IntegerField()
    loose = models.IntegerField()
    draw = models.IntegerField()
    logo_address = models.TextField()
    team_bio = models.TextField()
    language = models.ForeignKey(Language, on_delete=models.CASCADE)


class User(models.Model):
    user_fname = models.CharField(max_length=200)
    user_lname = models.CharField(max_length=200)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    is_head = models.BooleanField(default=False)
    email = models.TextField()
    skills = models.TextField()
    university = models.ForeignKey(University, on_delete=models.CASCADE)
