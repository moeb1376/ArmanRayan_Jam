from django.db import models
from main.models import Competition
from register.models import Team
from django.utils.translation import ugettext_lazy as _


# Create your models here.
class Cup(models.Model):
    cup_number = models.IntegerField(verbose_name=_("Cup Number"))
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, verbose_name=_("Competition"))
    team = models.ForeignKey(Team, on_delete=models.CASCADE, verbose_name=_("Team"))

    def __str__(self):
        return self.team.user_team.username + str(self.cup_number)

    class Meta:
        verbose_name = _("SPC Cup")
        verbose_name_plural = _("SPC Cups")
        ordering = ['competition']


class Tournament(models.Model):
    date = models.DateTimeField()
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
