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

class SearchISBN(models.Model):
    Year = models.IntegerField()
    P = models.IntegerField()

    def __unicode__(self):
        return self.Year

class Searchcsv(models.Model):
    Year = models.IntegerField()
    P = models.CharField(max_length = 200)
    def searcha(self):
        username = isbn
        with open('C:\\Users\\prasadv\\Desktop\\Stock Opt\\Clustering output file\ISBN_Data_SOMCluster_Period_nrm.csv', 'rt') as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                for field in row:
                    if field == username:
                        lista = row[29:-1] #lista is the range starting from p1 to p#
                        listb = [int(i[0]) for i in row[11:12]] # taking only the month from the list row
                        listb = listb[0] # listb is the month of the ISBN. here its converted from list to integer
                        listc = row[10:11]
                        listc = listc[0]
                        listc = listc.split('/')
                        listc = listc[0]
                        print (listc)
                        if listb == 1:
                            a = 12
                            b = (len(lista)/12)
                            if isinstance(b,float)==True:
                                b = math.ceil(b)
                            for j in range(1,b):
                                if a == 12:
                                    parts = lista[0:a]
                                    print (parts)
                                else:
                                    parts = lista[a:a+12]
                                    print (parts)
                            a = a + 12
                            return parts
                    else:
                        for i in range(0,listb):
                            lista.insert(0,0)
                            #print(len(lista))
                            a = 12
                            b = (len(lista)/12)
                            if isinstance(b,float)==True:
                                b = math.ceil(b)
                        for j in range(1,b):
                            if a == 12:
                                parts = lista[0:a]
                                print (parts)
                            else:
                                parts = lista[a:a+12]
                                print (parts)
                            a = a + 12
                            return parts
    def Publish(self):
        self.Year = listc
        self.P = parts
        
                               
    def __unicode__(self):
            return self.isbn
    
    
