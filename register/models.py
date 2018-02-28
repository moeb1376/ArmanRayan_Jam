from django.db import models
from main.models import *
from Jam.settings import const
from django.contrib.auth.models import User as auth_user
from django.contrib.auth import authenticate
from django.contrib.auth.models import AbstractUser


# Create your models here.
# class MyAuthUser(AbstractUser):
#     email = models.EmailField(unique=True)
#
class Test(models.Model):
    image = models.ImageField()


class Team(models.Model):
    user_team = models.ForeignKey(auth_user, on_delete=models.CASCADE, related_name='Teams')  # username = team_name
    rating = models.IntegerField(default=3)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    code_address = models.TextField(default='')
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    win = models.IntegerField(default=0)
    loose = models.IntegerField(default=0)
    draw = models.IntegerField(default=0)
    logo_address = models.TextField(default='')
    team_bio = models.TextField(default='')
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    mentor = models.CharField(max_length=20, null=True)
    # mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)

    def __str__(self):
        return self.user_team.username


class User(models.Model):
    user_fname = models.CharField(max_length=200)
    user_lname = models.CharField(max_length=200)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='Users')
    is_head = models.BooleanField(default=False)
    email = models.EmailField()
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, default=None)
    skills = models.TextField(default='')
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    entrance_year = models.IntegerField(default=1396)
    graduate_year = models.IntegerField(default=1400)

    def create_by_form(self, post_form, team, university, is_head=False):
        self.user_fname = post_form['f_name']
        self.user_lname = post_form['l_name']
        self.team = team
        self.is_head = is_head
        self.email = post_form['email']
        self.university = university
        # self.grade = grade

    def __str__(self):
        return self.user_fname + ' ' + self.user_lname
