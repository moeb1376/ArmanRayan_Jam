from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class Competition(models.Model):
    competition_name = models.CharField(max_length=200)
    competition_level = models.IntegerField()

    def __str__(self):
        return self.competition_name

    class Meta:
        ordering = ['competition_level']


class Grade(models.Model):
    grade_name = models.CharField(max_length=200)

    def __str__(self):
        return self.grade_name

    class Meta:
        ordering = ['grade_name']


class University(models.Model):
    university_name = models.CharField(max_length=200)
    university_city = models.CharField(max_length=200)

    def __str__(self):
        return self.university_name

    class Meta:
        ordering = ['university_name']


class Language(models.Model):
    language_name = models.CharField(max_length=200)

    def __str__(self):
        return self.language_name

    class Meta:
        ordering = ['language_name']


class Mentor(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    code = models.CharField(max_length=6)
    university = models.ForeignKey(University, on_delete=models.CASCADE)

    class Meta:
        ordering = ["first_name"]

    def __str__(self):
        return self.first_name + ' ' + self.last_name + '|' + self.university.university_name
