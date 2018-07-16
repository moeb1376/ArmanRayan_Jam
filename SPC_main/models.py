from django.db import models
from main.models import Competition
from register.models import Team


# Create your models here.
class Cup(models.Model):
    cup_number = models.IntegerField()
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    def __str__(self):
        return self.team.user_team.username + str(self.cup_number)


class Tournament(models.Model):
    date = models.DateTimeField()
    competition = models.ForeignKey(Competition,on_delete=models.CASCADE)


