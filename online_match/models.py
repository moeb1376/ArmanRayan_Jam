from django.db import models
from register.models import Team
from django.db.models.signals import post_save, pre_save
from django.utils.timezone import now, datetime, localdate
from django.dispatch import receiver
from django.core.validators import MinValueValidator, MaxValueValidator
from Jam.settings import MEDIA_ROOT, BASE_DIR, MEDIA_URL
import os
from hashlib import sha256
from datetime import date


# Create your models here.

def upload_match_log(instance, filename):
    type = filename.split('.')[-1]
    competition_name = 'SPC' if instance.team1.competition.competition_level < 3 else 'IAC'
    team_id = str(instance.team1.id) + "VS"
    team_id += str(instance.team2.id)
    logo_name = (str(team_id) + filename.split('.')[0]).encode()
    return "Logs/%s/%s/%s.%s" % (competition_name, team_id, sha256(logo_name).hexdigest(), type)


class Match(models.Model):
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="Team1")
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="Team2")
    is_running = models.BooleanField(default=False, blank=True)
    log_file = models.FileField(null=True, blank=True, upload_to=upload_match_log)
    # winner = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="Winner_team", blank=True, null=True)
    winner = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(2)])
    date = models.DateField(default=now)

    def __str__(self):
        return self.team1.user_team.username + " vs " + self.team2.user_team.username


def upload_code_address(instance, filename):
    type = filename.split('.')[-1]
    competition_name = 'SPC' if instance.team.competition.competition_level < 3 else 'IAC'
    team_id = instance.team.id
    logo_name = (str(team_id) + filename.split('.')[0]).encode()
    return "Codes/%s/%d/%s.%s" % (competition_name, team_id, sha256(logo_name).hexdigest(), type)


class Code(models.Model):
    code = models.FileField(null=True, blank=True, upload_to=upload_code_address)
    version = models.IntegerField(default=0, null=True, blank=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='Team_Code')

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
    print("pre_save", s, instance)
