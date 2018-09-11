import random
import time

from django.db import models
from register.models import Team
from django.db.models.signals import post_save, pre_save
from django.utils.timezone import now, datetime, localdate
from django.dispatch import receiver
from django.core.validators import MinValueValidator, MaxValueValidator
from Jam.settings import MEDIA_ROOT, BASE_DIR, MEDIA_URL
import os
from hashlib import sha256
from django.conf import settings
from django.core.mail import send_mail


# Create your models here.

def upload_match_log(instance, filename):
    type = filename.split('.')[-1]
    competition_name = 'SPC' if instance.team1.competition.competition_level < 3 else 'IAC'
    team_id = str(instance.team1.id) + "_VS_"
    team_id += str(instance.team2.id)
    logo_name = (str(team_id) + filename.split('.')[0]).encode()
    return "Logs/%s/%s/%s.%s" % (competition_name, team_id, sha256(logo_name).hexdigest(), type)


class Match(models.Model):
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="Team1")
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="Team2")
    is_running = models.BooleanField(default=False, blank=True)
    log_file = models.CharField(max_length=300, default="", null=True, blank=True)
    winner = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(2)])
    date = models.DateField(default=now)
    description = models.CharField(blank=True, null=True, max_length=200)

    def __str__(self):
        return self.team1.user_team.username + " vs " + self.team2.user_team.username


def upload_code_address(instance, filename):
    type = filename.split('.')[-1]
    competition_name = 'SPC' if instance.team.competition.competition_level < 3 else 'IAC'
    team_id = instance.team.id
    hash_name = sha256((str(team_id) + filename.split('.')[0]).encode()).hexdigest()
    random_int = random.randint(0, len(hash_name) - 5)
    secret_key = hash_name[random_int:random_int + 4]
    date = time.strftime("%y%m%d_%H%M%S")
    return "Codes/%s/%d/%d_%s_%s.%s" % (competition_name, team_id, team_id, date, secret_key, type)


class Code(models.Model):
    code = models.FileField(null=True, blank=True, upload_to=upload_code_address)
    version = models.IntegerField(default=0, null=True, blank=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='Team_Code')
    human_checked = models.BooleanField(blank=True, default=False, verbose_name="Checked")

    def __str__(self):
        return self.team.user_team.username + ' | V' + str(self.version)


@receiver(post_save, sender=Code)
def create_code(sender, instance, created, **kwargs):
    s = Code.objects.filter(team=instance.team).last()
    print('Post_save', s)
    if created:
        team = Team.objects.filter(pk=instance.team.id).update(code_address=instance.code)
        instance.team.code_address = instance.code
        print(team, instance.team.code_address)


@receiver(pre_save, sender=Code)
def set_version(sender, instance, **kwargs):
    query = Code.objects.filter(team=instance.team)
    if len(query) == 0:
        instance.version = 0
        return
    s = query.last().version
    instance.version = s + 1
    if len(query) > 4:
        first_code = query.first()
        os.remove(os.path.join(MEDIA_ROOT, os.path.relpath(first_code.code.url, MEDIA_URL)))
        first_code.delete()
    # emails = ['ebimosi14@gmail.com']
    emails = ['v_savabieh@yahoo.com', 'v.savabieh12@gmail.com', 'ebimosi14@gmail.com', 'j.agheleh@yahoo.com']
    messages = ['تیم ' + instance.team.user_team.username, 'در مسابقات ' + instance.team.competition.competition_name,
                'کد آپلود کرد.', instance.team.user_team.email]
    message = '\n'.join(messages)
    send_mail('جام بزرگ آرمانکده', message, settings.EMAIL_HOST_USER, emails)
    print("pre_save", s, instance)
