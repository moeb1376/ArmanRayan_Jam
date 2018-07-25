from django.core.mail import send_mail
from django.db import models
from main.models import *
from Jam.settings import const
from django.contrib.auth.models import User as auth_user
from django.contrib.auth import authenticate
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from hashlib import sha256
from django.db.models.signals import pre_save
from django.dispatch import receiver


# Create your models here.


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
    mentor = models.CharField(max_length=6, blank=True, default='')
    phone_number = models.CharField(max_length=11, blank=True, default='')

    def __str__(self):
        return self.user_team.username

    def total_games(self):
        return self.win + self.loose + self.draw

    def get_points(self):
        return self.win * 3 + self.draw


@receiver(pre_save, sender=Team)
def create_team(sender, instance, **kwargs):
    messages = ['تیم ' + instance.user_team.username,
                'در مسابقات ' + instance.competition.competition_name,
                'ثبت نام کرد.', instance.user_team.email]
    message = '\n'.join(messages)
    send_mail('جام بزرگ آرمانکده', message, settings.EMAIL_HOST_USER,
              ['v.savabieh12@gmail.com', 'ebimosi14@gmail.com'])


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

    def get_normal_entrance_year(self):
        return self.entrance_year % 100

    def __str__(self):
        return self.user_fname + ' ' + self.user_lname
