from django.db import models
from main.models import *
from Jam.settings import const
from django.contrib.auth.models import User as auth_user
from django.contrib.auth import authenticate


# Create your models here.

class Team(models.Model):
    user_team = models.ForeignKey(auth_user, on_delete=models.CASCADE)  # username = team_name
    # team_name = models.CharField(max_length=200, )
    # email = models.TextField()
    # password = models.CharField(max_length=200)
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

    def create_by_form(self, post_form, competition, university, languages):
        print('post form', post_form)
        temp_user = auth_user.objects.create_user(post_form['team_name'], post_form['email'], post_form['password'])
        temp_user.save()
        self.user_team = temp_user
        # self.team_name = post_form['team_name']
        # self.email = post_form['email']
        # self.password = post_form['password']
        self.competition = competition
        self.university = university
        self.language = languages
        self.code_address = const['CODE_DIRECTORY'] % (self.competition.id, self.user_team.username)
        self.logo_address = const['LOGO_DIRECTORY'] % (self.competition.id, self.user_team.username)

    def __str__(self):
        return self.user_team.username


class User(models.Model):
    user_fname = models.CharField(max_length=200)
    user_lname = models.CharField(max_length=200)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    is_head = models.BooleanField(default=False)
    email = models.TextField()
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, default=None)
    skills = models.TextField(default='')
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    entrance_year = models.IntegerField()
    graduate_year = models.IntegerField()
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