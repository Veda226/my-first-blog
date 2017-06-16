# Create your models here.
from django.db import models
from django.utils import timezone
import csv
import math
import datetime
import calendar


class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

'''class SearchISBN(models.Model):
    Year = models.IntegerField()
    P = models.IntegerField()

    def __unicode__(self):
        return self.Year'''


class Person(models.Model):
    Year = models.IntegerField()
    Jan = models.IntegerField()
    Feb = models.IntegerField()
    Mar = models.IntegerField()
    Apr = models.IntegerField()
    May = models.IntegerField()
    Jun = models.IntegerField()
    Jul = models.IntegerField()
    Aug = models.IntegerField()
    Sep = models.IntegerField()
    Oct = models.IntegerField()
    Nov = models.IntegerField()
    Dec = models.IntegerField()
    
