from django.core.mail import send_mail
from main.models import *
from django.contrib.auth.models import User as auth_user
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from hashlib import sha256
from django.db.models.signals import pre_save
from django.dispatch import receiver


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
    accuracy = models.FloatField(default=0.0)
    logo_image = models.ImageField(null=True, default='unknown.jpg',
                                   width_field="width_field",
                                   height_field="height_field",
                                   upload_to=upload_location)
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    team_bio = models.TextField(default='', blank=True)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    mentor = models.CharField(max_length=6, blank=True, default='')
    phone_number = models.CharField(max_length=11,default='')

    def __str__(self):
        return self.user_team.username

    def total_games(self):
        return self.win + self.loose + self.draw

    def get_points(self):
        if self.competition.competition_level < 3:
            return self.win * 3 + self.draw
        else:
            return self.accuracy

    @staticmethod
    def set_rating():
        for level in range(3, 6):
            print(level)
            objects = Team.objects.filter(competition__competition_level=level).order_by("-accuracy")
            print('objects', objects)
            len_objects = len(objects)
            a = round(len_objects * 0.2)
            b = a + round(len_objects * 0.5)
            count = 0
            while count < b and b != 0:
                print("\t count", count)
                temp = objects[count]
                rate = 1 if count < a else 2
                temp.rating = rate
                temp.save()
                count += 1
                while count < len_objects and temp.accuracy == objects[count].accuracy:
                    temp = objects[count]
                    temp.rating = rate
                    temp.save()
                    count += 1
            for i in range(count, len_objects):
                temp = objects[i]
                temp.rating = 3
                temp.save()


@receiver(pre_save, sender=Team)
def create_team(sender, instance, **kwargs):
    messages = ['تیم ' + instance.user_team.username,
                'در مسابقات ' + instance.competition.competition_name,
                'ثبت نام کرد.', instance.user_team.email]
    message = '\n'.join(messages)
    # send_mail('جام بزرگ آرمانکده', message, settings.EMAIL_HOST_USER,
    #           ['v.savabieh12@gmail.com', 'ebimosi14@gmail.com'])


class MyUser(models.Model):
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

    def get_fname_lname(self):
        return self.user_fname+' '+self.user_lname

    def __str__(self):
        return self.user_fname + ' ' + self.user_lname
