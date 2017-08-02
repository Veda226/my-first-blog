from django.shortcuts import render
from .models import Post
from .models import Person
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from django.shortcuts import redirect
from .SearchCSV import searchISBN
from .tables import PersonTable
from django_tables2 import RequestConfig
import csv
import math
import datetime
import calendar
import pandas as pd
from bokeh.charts import Line, output_file, show, Bar
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource, LabelSet, Label, HoverTool, ranges, Range1d
import calendar
from datetime import *
from bokeh.io import *
from bokeh.palettes import PuBu
import pygal

bar_chart = pygal.Bar()


# Create your views here.
def post_list(request):
    return render(request, 'blog/post_list.html', {})


def submit(request):
    myList = request.POST.get('myList', False)
    myList1 = request.POST.get('dropdown-menu', False)
    return render(request, 'blog/test.html', {'myList': myList})


def predict(request):
    myList = request.POST.get('myList', False)
    myList1 = request.POST.get('dropdown-menu', False)
    return render(request, 'blog/predict.html')


def Pricing(request):
    # Command(myList)
    return render(request, 'blog/Pricing.html')


def SalesData(request):
    if request.method == 'POST':
        isbn = request.POST.get('isbn')
        if isbn == "":
            return render(request, 'blog/predict.html')
        else:
            username = isbn
            # HTML text is assigned to the html_str variable. Ideally this will be writen to the file ISBN2.html
            html_str = """{% extends 'blog/base.html' %}{% block content %}{% load staticfiles %}<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"><script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script><script type="text/javascript" src="http://jqueryrotate.googlecode.com/svn/trunk/jQueryRotate.js"></script><script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script><div class="container"><div class="panel-group">"""
            #   ISBN2.HTML file is opened in the below with condition
            with open('U:\\django_test\\mysitetest\\blog\\templates\\blog\ISBN2.html', 'w') as myfile:
                # with the file open,
                
                myfile.write(html_str)
                myfile.write("""<div class="panel panel-default"><div class="panel-heading"><h4 class="panel-title"><a data-toggle="collapse" href="#collapse1">Current Edition</a></h4></div><div id="collapse1" class="panel-collapse collapse"><div class="panel-body"><br/><div class="bs-example" data-example-id="table table-bordered" id ="table table-bordered"><table class= "table table-bordered"> <thead> <th class=""col-md-1"">""" + "Year" + """</th><th class=""col-md-1"">Jan</th> <th>Feb</th> <th>Mar</th> <th>Apr</th> <th>May</th> <th>Jun</th> <th>Jul</th> <th>Aug</th> <th>Sep</th> <th>Oct</th> <th>Nov</th> <th>Dec</th></tr> </thead> <tbody> <tr> """)
                
                with open('C:\\Users\\prasadv\\Desktop\\Stock Opt\\Clustering output file\ISBN_Data_SOMCluster_Period_nrm.csv','rt') as f:
                    reader = pd.read_csv(f,delimiter = ',')
                    df1=pd.DataFrame(reader,columns = ['','ISBN','PMG','PMC','Medium','Extended Medium','Edition Type','First Sale Time','First Sale Month','Sale Period(in Months)','Quarter','First Year Sales','Second Year Sales','Third Year Sales','Fourth Year Sales','Fifth Year Sales','Supply Site : L','Supply Site : R','Range Sales Cluster','Previous ISBN','Previous Edition Cluster','SOM Cluster','Cluster : 2-12','Cluster : 1-12','Cluster : 13-24','Cluster : 25-36','Cluster : 37-48','Cluster : 49-60','Cluster : 1-24','Cluster : 1-36','Cluster : 1-48','Cluster : 1-60','Period : 1','Period : 2','Period : 3','Period : 4','Period : 5','Period : 6','Period : 7','Period : 8','Period : 9','Period : 10','Period : 11','Period : 12','Period : 13','Period : 14','Period : 15','Period : 16','Period : 17','Period : 18','Period : 19','Period : 20','Period : 21','Period : 22','Period : 23',	'Period : 24',	'Period : 25',	'Period : 26',	'Period : 27',	'Period : 28',	'Period : 29',	'Period : 30',	'Period : 31',	'Period : 32',	'Period : 33',	'Period : 34',	'Period : 35',	'Period : 36',	'Period : 37',	'Period : 38',	'Period : 39',	'Period : 40',	'Period : 41',	'Period : 42',	'Period : 43',	'Period : 44',	'Period : 45',	'Period : 46',	'Period : 47',	'Period : 48',	'Period : 49',	'Period : 50',	'Period : 51',	'Period : 52',	'Period : 53',	'Period : 54',	'Period : 55',	'Period : 56',	'Period : 57',	'Period : 58',	'Period : 59',	'Period : 60',	'Period : 61',	'Period : 62',	'Period : 63',	'Period : 64',	'Period : 65',	'Period : 66',	'Period : 67',	'Period : 68',	'Period : 69',	'Period : 70',	'Period : 71',	'Period : 72',	'Period : 73',	'Period : 74',	'Period : 75',	'Period : 76',	'Period : 77',	'Period : 78',	'Period : 79',	'Period : 80',	'Period : 81',	'Period : 82',	'Period : 83',	'Period : 84',	'Period : 85',	'Period : 86',	'Period : 87',	'Period : 88',	'Period : 89',	'Period : 90',	'Period : 91',	'Period : 92',	'Period : 93',	'Period : 94',	'Period : 95',	'Period : 96',	'Period : 97',	'Period : 98',	'Period : 99',	'Period : 100',	'Period : 101',	'Period : 102',	'Period : 103',	'Period : 104',	'Period : 105',	'Period : 106',	'Period : 107',	'Period : 108',	'Period : 109',	'Period : 110',	'Period : 111',	'Period : 112',	'Period : 113',	'Period : 114',	'Total Sales'])
                    GG = df1[df1['ISBN'].notnull() & (df1['ISBN'] == float(username))]
                    lista = GG.loc[:,'Period : 1':'Period : 114']#lista is the range starting from p1 to p#
                    lista = lista.values.tolist()
                    lista = [item for sublist in lista for item in sublist ]
                    lista = list(map(int, lista))
                    max_num = max(list(map(int, lista)))
                    listb = GG.loc[:,'First Sale Month'] # taking only the month from the list row
                    listc = GG.loc[:,'First Sale Time']
                    listc=''.join(listc.tolist())
                    listc = listc.split('/')
                    listc = listc[0]
                    listb = listb.get_value(listb.index[0])
                    myfile.write("<td>" + listc + "</td>")
                    date1 = datetime.strptime(str(listc) + "-1-1", "%Y-%m-%d")
                    if int(listb) == 1:
                        a = 12
                        b = (len(lista) / 12)
                        if isinstance(b, float) == True:
                            b = math.ceil(b)
                        for j in range(1, b):
                            if a == 12:
                                parts = lista[0:a]
                                pd_new = pd.DataFrame(parts)
                                Part_for_chart = parts
                                parts = ['<td>' + str(s) + '</td>' for s in parts]
                                str1 = ''.join(parts)
                                myfile.write(str1 + "</tr>")
                                a = a + 12
                            else:
                                parts = lista[a - 12:a]
                                if (len(parts)) != 12:
                                    lengthofparts = 12 - (len(parts))
                                    g = [parts.append(0) for z in range(0, lengthofparts)]
                                pd_new = pd_new.append(parts)
                                for x in parts:
                                    Part_for_chart.append(x)
                                parts = ['<td>' + str(s) + '</td>' for s in parts]
                                str1 = ''.join(parts)
                                listd = '<td>' + str(int(listc) + 1) + '</td>'
                                myfile.write(listd + str1 + "</tr>")
                                a = a + 12
                                listc = int(listc) + 1
                    else:
                        for i in range(0, listb):
                            lista.insert(0, 0)
                        a = 12
                        b = (len(lista) / 12)
                        if isinstance(b, float) == True:
                            b = math.ceil(b)
                        for j in range(1, b):
                            if a == 12:
                                parts = lista[0:a]
                                pd_new = pd.DataFrame(parts)
                                Part_for_chart = parts
                                parts = ['<td>' + str(s) + '</td>' for s in parts]
                                str1 = ''.join(parts)
                                myfile.write(str1 + "</tr>")
                                a = a + 12
                            else:
                                parts = lista[a:a + 12]
                                if (len(parts)) != 12:
                                    lengthofparts = 12 - (len(parts))
                                    g = [parts.append(0) for z in range(0, lengthofparts)]
                                pd_new = pd_new.append(parts)
                                for x in parts:
                                    Part_for_chart.append(x)
                                parts = ['<td>' + str(s) + '</td>' for s in parts]
                                str1 = ''.join(parts)
                                listd = '<td>' + str(int(listc) + 1) + '</td>'
                                myfile.write(listd + str1 + "</tr>")
                                a = a + 12
                                listc = int(listc) + 1
                    date2 = datetime.strptime(str(listc + 1) + "-1-01", "%Y-%m-%d")
                    months_str = calendar.month_name
                    months = []
                    while date1 < date2:
                        month = date1.month
                        year = date1.year
                        month_str = months_str[month][0:3]
                        months.append("{0}-{1}".format(month_str, str(year)[-2:]))
                        next_month = month + 1 if month != 12 else 1
                        next_year = year + 1 if next_month == 1 else year
                        date1 = date1.replace(month=next_month, year=next_year)
                    source = ColumnDataSource(data=dict(height=Part_for_chart, weight=months, names=Part_for_chart))
                    output_file("U:\\django_test\\mysitetest\\blog\\templates\\svg\\bar.svg")
                    HoverTool(tooltips=[('date', '@date{%F}'),
                                        ('close', '$@{adj close}{%0.2f}'),
                                        # use @{ } for field names with spaces
                                        ('volume', '@volume{0.00 a}'),
                                        ],
                              # display a tooltip whenever the cursor is vertically in line with a glyph
                              mode='vline'
                              )
                    p = figure(plot_width=1500, title=username+'- (Current Edition)', tools="",
                               x_range=source.data["weight"],
                               y_range=ranges.Range1d(start=0, end=(max_num + 100)), toolbar_location=None)
                    p.line(months, Part_for_chart, line_width=2)
                    labels = LabelSet(x='weight', y='height', text='height', level='glyph', x_offset=-13.5,
                                      y_offset=0, source=source, text_font_size="10pt", render_mode='canvas')
                    p.xaxis.major_label_orientation = math.pi / 2
                    p.add_layout(labels)
                    save(p)
                myfile.write(
                    """<table class="inlineTable"><div id="chart" >{% include "svg/bar.svg" %}</div></table><div class="panel-footer">@Copyright Elsevier 2017. Created by v.prasad@elsevier.com</div></div></div></div></div></div></div>""")
                myfile.write("</tr>{% endblock content %}")
                myfile.close()
            return render(request, 'blog/ISBN2.html', )


def person_list(request):
    table = PersonTable(Person.objects.all())
    RequestConfig(request).configure(table)
    return render(request, 'blog/person_list.html', {'table': table})


def chart(request):
    bar_chart = pygal.Bar(fill=True, style=BlueStyle)  # Then create a bar graph object
    bar_chart.add('blue', [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55])  # Add some values
    chart = bar_chart.render_django_response()  # Save the svg to a file
    return render(request, 'svg/bar_chart.SVG', {'chart': chart}, content_type='image/svg+xml')


