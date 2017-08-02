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
                global Part_for_chart
                #with open('C:\\Users\\prasadv\\Desktop\\Stock Opt\\Clustering output file\ISBN_Data_SOMCluster_Period_nrm.csv','rt') as f:
                with open('C:\\Users\\prasadv\\Desktop\\Stock Opt\\Clustering output file\Consolidation_meta.csv','rt') as f:
                    reader = pd.read_csv(f,delimiter = ',')                     # the csv file is read here
                    df=pd.DataFrame(reader)                                     # the csv file is converted to a dataframe
                    new_header = df.iloc[0]                                     # headers are pulled from the read file, and passed to new_header variable
                    df1 = df[1:] 
                    df1.rename(columns = new_header)                            # Adding headers to the dataframe
                    GG = df1.loc[(df1['ISBN'] == username)]                     #searching the ISBN in the dataframe
                    if not GG.empty:
                        print(GG)
                        previous_isbn = GG.filter(items=['Previous EDITION(-1)'])
                        previous_isbn = previous_isbn.values.tolist()
                        previous_isbn = [item for sublist in previous_isbn for item in sublist ]
                        print(previous_isbn)
                        previous_isbn_1 = GG.filter(items=['Previous EDITION(-2)'])
                        previous_isbn_1 = previous_isbn_1.values.tolist()
                        previous_isbn_1 = [item for sublist in previous_isbn_1 for item in sublist ]
                        print(previous_isbn_1)
                        aa = []
                        if previous_isbn:
                            GG1 = df1.loc[(df1['PIN'] == previous_isbn[0])]
                            print(GG1)
                        if previous_isbn_1:
                            GG2 = df1.loc[(df1['PIN'] == previous_isbn_1[0])]
                            print(GG2)
                        temp_meta = GG.filter(items=['ISBN','US_PUB_DATE','PMG','PMC','Medium','TITLE_DISC','AUTHOR']) #filtering the variable GG with the column for meta data
                        str1 = temp_meta.values.tolist()                            # converting the dataframe to list
                        str1 = [item for sublist in str1 for item in sublist ]      #reitering the convertion from dataframe to list
                        # writing the HTML tags for metadata table. and assining the values from str1 variable 
                        str_html_temp ="""<table class= "table table-bordered"><thead> <th class="col-sm-2" style="background-color:lightgrey;"> ISBN (0)</th> <td class="col-sm-2">""" + str(str1[0]) + """</td><th class="col-sm-2" style="background-color:lightgrey;"> PMG</th> <td class="col-sm-2">""" + str(str1[2])+ """</td><tr><th class="col-sm-2" style="background-color:lightgrey;"> Pub Date</th> <td class="col-sm-2">""" + str(str1[1]) +"""</td><th class="col-sm-2" style="background-color:lightgrey;"> PMC</th> <td class="col-sm-2">""" + str(str1[3]) + """</td></tr><tr><th class="col-sm-2" style="background-color:lightgrey;"> Medium</th> <td class="col-sm-2">""" + str(str1[4]) + """</td><th class="col-sm-2" style="background-color:lightgrey;"> Author</th> <td class="col-sm-2">""" + str(str1[6]) + """</td></tr><tr><th class="col-sm-2" style="background-color:lightgrey;">Title</th><td class="col-sm-2">""" + str(str1[5]) + """</td></tr></table>"""
                        # writing the HTML tages to ISBN2 file, these html tags are for meta data, with collapsable window
                        myfile.write("""<div class="panel panel-default"><div class="panel-heading"><h4 class="panel-title"><a data-toggle="collapse" href="#collapse1">MetaData</a></h4></div><div id="collapse1" class="panel-collapse collapse in"><div class="panel-body">""" +str_html_temp + """</div></div>""")
                        # writing the HTML tages to ISBN2 file, this sets up the table for current edition sales data
                        myfile.write("""<div class="panel panel-default"><div class="panel-heading"><h4 class="panel-title"><a data-toggle="collapse" href="#collapse2">Current Edition</a></h4></div><div id="collapse2" class="panel-collapse collapse"><div class="panel-body"><br/><div class="bs-example" data-example-id="table table-bordered" id ="table table-bordered"><table class= "table table-bordered"> <thead> <th class=""col-md-1"">""" + "Year" + """</th><th class=""col-md-1"">Jan</th> <th>Feb</th> <th>Mar</th> <th>Apr</th> <th>May</th> <th>Jun</th> <th>Jul</th> <th>Aug</th> <th>Sep</th> <th>Oct</th> <th>Nov</th> <th>Dec</th></tr> </thead> <tbody> <tr> """)
                        lista = GG.filter(regex=("Period.*"))                       # using regex, getting all period sales
                        lista = lista.values.tolist()                               # removing the headers from the dataframe
                        lista = [item for sublist in lista for item in sublist ]    # converting dataframe to list
                        lista = list(map(int, lista))                               # converting the list variables to integer
                        max_num = max(list(map(int, lista)))                        # getting the max number for future use
                        listb = GG.loc[:,'Month']                                   # taking only the month from the list row
                        listc = GG.loc[:,'First Sale Month']                        #taking the first sale month for preparing the table
                        listc=''.join(listc.tolist())
                        date1 = listc[0:8]                                               # this is used for creating a running date period for sales table[]
                        listc = listc[4:8]                                          #Getting only the year
                        listc = int(listc)
                        listb = listb.get_value(listb.index[0])                     # getting the month value
                        myfile.write("<td>" + str(listc) + "</td>")                      # writing the year to the ISBN2 file
                        # if the first sale month is january then the below set of the codes works
                        if int(listb) == 1:                     #condintion to check the first sale month equal to 1
                            a = 12                              #future use
                            b = (len(lista) / 12)               #Dividing the length of the period to get how many years the sales period has
                            if isinstance(b, float) == True:    # if the division results in value with decimal places, rounding off the decimal 
                                b = math.ceil(b)
                            for j in range(1, b):               # running the below loop based on number of years
                                if a == 12:                     # this condition is to check whether its the first year of sale, as it has to be handled differently
                                    parts = lista[0:a]          #assigning the values to the parts. This variable will be used for compliation purpose
                                    pd_new = pd.DataFrame(parts)#Converting the parts variable to dataframe
                                    Part_for_chart = parts      # assigning values to variable which will be used for charts
                                    parts = ['<td>' + str(s) + '</td>' for s in parts] # adding HTML tags for every element in the dataframe
                                    str1 = ''.join(parts)       # converting the dataframe into list
                                    myfile.write(str1 + "</tr>")# writing the str1 list to ISBN2 file
                                    a = a + 12
                                else:
                                    parts = lista[a - 12:a]     #adding the values to the parts
                                    if (len(parts)) != 12:      #in the last year of sales, it will not have 12 month data, hence its checked here. and if its true "0" will be added in the below code
                                        lengthofparts = 12 - (len(parts))
                                        g = [parts.append(0) for z in range(0, lengthofparts)]
                                    pd_new = pd_new.append(parts)
                                    for x in parts: # here appending every value into Part_for_chart variable.
                                        Part_for_chart.append(x)
                                    parts = ['<td>' + str(s) + '</td>' for s in parts]# adding html tags for sales table
                                    str1 = ''.join(parts)
                                    listd = '<td>' + str(int(listc) + 1) + '</td>'  # adding the year to the table with HTML tags
                                    myfile.write(listd + str1 + "</tr>")            #wRITING THE tags to the ISBN2 file
                                    a = a + 12
                                    listc = int(listc) 
                                    listc = listc + 1
                                    print(listc)
                            date2 = datetime.strptime(str(int(listc) + 1) + "-1-01", "%Y-%m-%d") # date2 variable to capture the last year
                            
                        else:
                            for i in range(0, listb):           # is the title doesnt have a sales start month as 1 then its pushed here
                                lista.insert(0, 0)              # 0's are inserted based the month number
                            a = 12                              #future use
                            b = (len(lista) / 12)               #same purpose as above. please refer line #96 to 119 for the below codes commentary
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
                                    listc = int(listc) + 1 # please refer line # 96 to 119 for commentary
                                    print(listc)
                        date2 = datetime.strptime(str(int(listc) + 1) + "-1-01", "%Y-%m-%d") # date2 variable to capture the last year
                        #date2 = datetime.strptime(str(listc + 1) + "-1-01", "%Y-%m-%d") # date2 variable will be used for creating the consecutive months and years for chart
                        months_str = calendar.month_name
                        months = []
                        date1 = datetime.strptime(date1,"%d/%m/%Y")
                        # below while loop will generate consecutive # of months and years which is stored into months variable
                        while date1 < date2:
                            month = date1.month # month is stored here.
                            year = date1.year   # year is stored here
                            month_str = months_str[month][0:3]  # month num is converted to string 1  is converted to Jan
                            months.append("{0}-{1}".format(month_str, str(year)[-2:]))  # month string is appended to months variable
                            next_month = month + 1 if month != 12 else 1
                            next_year = year + 1 if next_month == 1 else year
                            date1 = date1.replace(month=next_month, year=next_year)
                        source = ColumnDataSource(data=dict(height=Part_for_chart, weight=months, names=Part_for_chart))
                        output_file("U:\\django_test\\mysitetest\\blog\\templates\\svg\\bar.svg")
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
                            """<table class="inlineTable"><div id="chart" >{% include "svg/bar.svg" %}</div></table><div class="col-md-9">{% block test %}{% endblock %}</div><div class="panel-footer">@Copyright Elsevier 2017. Created by v.prasad@elsevier.com</div></div></div></div></div></div></div>""")
                        myfile.write("</tr>{% endblock content %}")
                    
                    else:
                        myfile.write("""<style>.alert { padding: 20px;   background-color: #f44336;    color: white;}.closebtn {    margin-left: 15px;color: white;    font-weight: bold;    float: right;    font-size: 22px;    line-height: 20px;    cursor: pointer;   ransition: 0.3s;}.closebtn:hover {    color: black;}</style></head><body><div class="alert">  <span class="closebtn" onclick="this.parentElement.style.display='none';">&times;</span>   <strong>ISBN missing in database:  </strong>The ISBN """ + username + """ is not in the database. Please search a different ISBN</div></body>{% endblock content %}""")
                    myfile.close()
            return render(request, 'blog/ISBN2.html', )
            return render(request, 'blog/test_to_extend.html')


def person_list(request):
    table = PersonTable(Person.objects.all())
    RequestConfig(request).configure(table)
    return render(request, 'blog/person_list.html', {'table': table})


def chart(request):
    bar_chart = pygal.Bar(fill=True, style=BlueStyle)  # Then create a bar graph object
    bar_chart.add('blue', [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55])  # Add some values
    chart = bar_chart.render_django_response()  # Save the svg to a file
    return render(request, 'svg/bar_chart.SVG', {'chart': chart}, content_type='image/svg+xml')


