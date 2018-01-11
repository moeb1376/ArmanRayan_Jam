from django.db import models


# Create your models here.
class Competition(models.Model):
    competition_name = models.CharField(max_length=200)
    competition_level = models.IntegerField()

    def __str__(self):
        return self.competition_name


class Grade(models.Model):
    grade_name = models.CharField(max_length=200)
    entrance_year = models.IntegerField()
    graduate_year = models.IntegerField()

    def __str__(self):
        return self.grade_name


class University(models.Model):
    university_name = models.CharField(max_length=200)
    university_city = models.CharField(max_length=200)

    def __str__(self):
        return self.university_name


class Language(models.Model):
    language_name = models.CharField(max_length=200)

    def __str__(self):
        return self.language_name
