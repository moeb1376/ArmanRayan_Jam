from django.db import models
from main.models import *
from Jam.settings import const


# Create your models here.

class Team(models.Model):
    team_name = models.CharField(max_length=200, )
    email = models.TextField()
    rating = models.IntegerField(default=3)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    code_address = models.TextField(default='')
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    password = models.CharField(max_length=200)
    win = models.IntegerField(default=0)
    loose = models.IntegerField(default=0)
    draw = models.IntegerField(default=0)
    logo_address = models.TextField(default='')
    team_bio = models.TextField(default='')
    language = models.ForeignKey(Language, on_delete=models.CASCADE)

    def create_by_form(self, post_form, competition, university, languages):
        self.team_name = post_form['team_name']
        self.email = post_form['email']
        self.competition = competition
        self.university = university
        self.code_address = const['CODE_DIRECTORY'].replace('team_name', self.team_name)
        self.password = post_form['password']
        self.logo_address = const['LOGO_DIRECTORY'].replace('team_name', self.team_name)
        self.language = languages

    def __str__(self):
        return self.team_name


class User(models.Model):
    user_fname = models.CharField(max_length=200)
    user_lname = models.CharField(max_length=200)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    is_head = models.BooleanField(default=False)
    email = models.TextField()
    skills = models.TextField(default='')
    university = models.ForeignKey(University, on_delete=models.CASCADE)

    def create_by_form(self, post_form, team, university, is_head=False):
        self.user_fname = post_form['f_name']
        self.user_lname = post_form['l_name']
        self.team = team
        self.is_head = is_head
        self.email = post_form['email']
        self.university = university

    def __str__(self):
        return self.user_fname + ' ' + self.user_lname
