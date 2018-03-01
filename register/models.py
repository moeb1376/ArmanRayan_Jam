from django.db import models
from main.models import *
from Jam.settings import const
from django.contrib.auth.models import User as auth_user
from django.contrib.auth import authenticate
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from hashlib import sha256


# Create your models here.
# class MyAuthUser(AbstractUser):
#     email = models.EmailField(unique=True)
#
def upload_test(instance, filename):
    return 'testi/%s.%s' % (instance.id, filename.split('.')[-1])


class Test(models.Model):
    image = models.ImageField(default=settings.LOGO_DEFAULT, upload_to=upload_test, width_field="width_field",
                              height_field="height_field", null=True, blank=True)
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)


def upload_location(instance, filename):
    type = filename.split('.')[-1]
    competition_name = 'SPC' if instance.competition.competition_level < 3 else 'IAC'
    team_id = instance.id
    logo_name = (str(team_id) + filename.split('.')[0]).encode()
    return "%s/%d/logo/%s.%s" % (competition_name, team_id, sha256(logo_name).hexdigest(), type)


class Team(models.Model):
    user_team = models.ForeignKey(auth_user, on_delete=models.CASCADE, related_name='Teams')  # username = team_name
    rating = models.IntegerField(default=3)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    code_address = models.TextField(default='', blank=True)
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    win = models.IntegerField(default=0)
    loose = models.IntegerField(default=0)
    draw = models.IntegerField(default=0)
    logo_image = models.ImageField(null=True, default='unknown.jpg',
                                   width_field="width_field",
                                   height_field="height_field",
                                   upload_to=upload_location)
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    team_bio = models.TextField(default='', blank=True)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    mentor = models.CharField(max_length=20, blank=True, default='')

    def __str__(self):
        return self.user_team.username


class MyUser(models.Model):
    #  id = models.IntegerField(primary_key=True)
    user_fname = models.CharField(max_length=200, blank=True)
    user_lname = models.CharField(max_length=200, blank=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='Users', blank=True)
    is_head = models.BooleanField(default=False)
    email = models.EmailField(blank=True)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, default='', blank=True, null=True)
    skills = models.TextField(blank=True)
    university = models.ForeignKey(University, on_delete=models.CASCADE, default='', blank=True, null=True)
    entrance_year = models.IntegerField(default=1396, blank=True)
    graduate_year = models.IntegerField(default=1400, blank=True)

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
