from django.db import models
from register.models import Team


# Create your models here.

class Match(models.Model):
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="Team1")
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="Team2")
    is_running = models.BooleanField(default=False, blank=True)
    log_file = models.FileField(null=True)

    def __str__(self):
        return self.team1.user_team.username + " vs " + self.team2.user_team.username


def upload_code_address(instance, filename):
    return "Codes/%s" % filename


class Code(models.Model):
    code = models.FileField(null=True, blank=True, upload_to=upload_code_address)
    version = models.IntegerField(default=0)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='Team_Code')

    def __str__(self):
        return self.team.user_team.username + ' | V' + str(self.version)
