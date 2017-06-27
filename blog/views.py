from django.shortcuts import render
from .models import Post
#from .models import SearchISBN, Searchcsv
from .models import Person
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
#from .forms import PostFormisbn
from django.shortcuts import redirect
from .SearchCSV import searchISBN
from .tables import PersonTable
from django_tables2 import RequestConfig
import pygal
from pygal.style import BlueStyle
import csv
import math
import datetime
import calendar
import pandas as pd
# Create your views here.
def post_list(request):
    return render(request, 'blog/post_list.html', {})
def submit(request):
    myList = request.POST.get('myList',False)
    myList1 = request.POST.get('dropdown-menu',False)
    return render(request, 'blog/test.html',{'myList':myList})

def predict(request):
    myList = request.POST.get('myList',False)
    myList1 = request.POST.get('dropdown-menu',False)
    return render(request, 'blog/predict.html')

def Pricing(request):
    #Command(myList)
    return render(request, 'blog/Pricing.html')

def SalesData(request):
    if request.method == 'POST':
        isbn = request.POST.get('isbn')
        username = isbn
        html_str = """{% extends 'blog/base.html' %}{% block content %}{% load staticfiles %}<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"><script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script><script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script><div class="bs-example" data-example-id="striped-table"><table class=" table-striped"> <thead> <tr> """
        with open('U:\\django_test\\mysitetest\\blog\\templates\\blog\ISBN2.html','w') as myfile:
            myfile.write(html_str)
            myfile.write("<th>"+username+"</th><th>January</th> <th>February</th> <th>March</th> <th>April</th> <th>May</th> <th>June</th> <th>July</th> <th>August</th> <th>September</th> <th>October</th> <th>November</th> <th>December</th></tr> </thead> <tbody> <tr> ")
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
                            myfile.write("<td>"+listc+"</td>")
                            if listb == 1:
                                a = 12
                                b = (len(lista)/12)
                                if isinstance(b,float)==True:
                                    b = math.ceil(b)
                                for j in range(1,b):
                                    if a == 12:
                                        parts = lista[0:a]
                                        parts = ['<td>'+ str(s) + '</td>' for s in parts]
                                        str1 = ''.join(parts)
                                        myfile.write(str1+"</tr>")
                                        print (parts)
                                        a = a + 12
                                    else:
                                        parts = lista[a-12:a]
                                        parts = ['<td>'+ str(s) + '</td>' for s in parts]
                                        str1 = ''.join(parts)
                                        
                                        myfile.write(str1+"</tr>")
                                        print (parts)
                                        a = a + 12                            
                                print(a)
                            else:
                                for i in range(0,listb):
                                    lista.insert(0,0)
                                a = 12
                                b = (len(lista)/12)                       
                                if isinstance(b,float)==True:
                                    b = math.ceil(b)
                            for j in range(1,b):
                                if a == 12:
                                     parts = lista[0:a]
                                     parts = ['<td>'+ str(s) + '</td>' for s in parts]
                                     str1 = ''.join(parts)
                                     #listd = '<td>'+ str(int(listc)+1) + '</td>'
                                     myfile.write(str1+"</tr>")
                                     print (parts)
                                else:
                                     parts = lista[a:a+12]
                                     parts = ['<td>'+ str(s) + '</td>' for s in parts]
                                     str1 = ''.join(parts)
                                     listc = int(listc)+1
                                     listd = '<td>'+ str(int(listc)+1) + '</td>'
                                     myfile.write(listd + str1+"</tr>")
                                     print (parts)
                                a = a + 12
                            
            myfile.write("</tr>{% endblock content %}")
            myfile.close()
        return render(request, 'blog/ISBN2.html',)
    
def person_list(request):
    table = PersonTable(Person.objects.all())
    RequestConfig(request).configure(table)
    return render(request, 'blog/person_list.html', {'table': table})


def chart(request):
    bar_chart = pygal.Bar(fill=True, style=BlueStyle)     # Then create a bar graph object
    bar_chart.add('blue', [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55])  # Add some values
    chart = bar_chart.render_django_response()                          # Save the svg to a file
    return render( request,'svg/bar_chart.SVG', {'chart':chart}, content_type='image/svg+xml')
