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
import re
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
            with open('U:\\django_test\\mysitetest\\blog\\templates\\blog\ISBN2.html', 'w') as myfile:
                myfile.write(html_str)
                # with the file open,
                global Part_for_chart
                with open('C:\\Users\\prasadv\\Desktop\\Stock Opt\\Clustering output file\Consolidation_meta.csv','rt') as f:
                    z = 0
                    reader = pd.read_csv(f,delimiter = ',')                     # the csv file is read here
                    reader = reader.fillna(value=0)
                    df=pd.DataFrame(reader)
                    df['ISBN'] = pd.to_numeric(df['ISBN'], errors='coerce')
                    warehouses = ['L','R','BOTH']                                        # the csv file is converted to a dataframe
                    check_linn = 0
                    for j in range(0,3):
                        k = 2
                        str_Html_L_R,GG = Linn_Rushden(df,warehouses[j],username,k)
                        z = z + 1
                        if not GG.empty:                                            #checking whether data frame for the ISBN exist
                            previous_isbn = GG.filter(items=['Previous EDITION(-1)'])
                            previous_isbn = previous_isbn.values.tolist()
                            previous_isbn = [item for sublist in previous_isbn for item in sublist ]
                            previous_isbn_1 = GG.filter(items=['Previous EDITION(-2)'])
                            previous_isbn_1 = previous_isbn_1.values.tolist()
                            previous_isbn_1 = [item for sublist in previous_isbn_1 for item in sublist ]
                            aa = []
                            if warehouses[j] == "L":
                                check_linn=1
    ###############################################################################################################################################################################################
                            # in the below if condition, previous edition pin is searched and the row data is pulled, and sent function called test for creating ISBN1.html and the file is closed
    ###############################################################################################################################################################################################                        
                            if previous_isbn:
                                GG1 = df.loc[(df['PIN'] == previous_isbn[0])]
                                edition = 1
                                if not GG1.empty:
                                    previous_isbn_num=GG1.filter(items=['ISBN','US_PUB_DATE'])
                                    str_Html_previous = test(GG1,edition,"Previous Edition-",warehouses[j])
                                    with open('U:\\django_test\\mysitetest\\blog\\templates\\blog\ISBN'+ str(edition) +'.html', 'w') as myfile2:
                                        myfile2.write(str_Html_previous)
                                        myfile2.close()
                                    previous_isbn_num = previous_isbn_num.values.tolist()                            # converting the dataframe to list
                                    previous_isbn_num = [item for sublist in previous_isbn_num for item in sublist ]      #reitering the convertion from dataframe to list
                                else:
                                    previous_isbn_num = ["-","-"]
    ###############################################################################################################################################################################################
                            # previous, pervious ISBN is searched and row data is pulled, ISBN0. html is crated, and the file is closed
    ###############################################################################################################################################################################################
                            if previous_isbn_1:
                                GG2 = df.loc[(df['PIN'] == previous_isbn_1[0])]
                                edition = 0
                                if not GG2.empty:
                                    #print(GG2)
                                    previous_isbn_num_1=GG2.filter(items=['ISBN','US_PUB_DATE'])
                                    str_Html_previous = test(GG2,edition,"Previous Edition-",warehouses[j])
                                    with open('U:\\django_test\\mysitetest\\blog\\templates\\blog\ISBN'+ str(edition) +'.html', 'w') as myfile1:
                                        myfile1.write(str_Html_previous)
                                        myfile1.close()
                                    previous_isbn_num_1 = previous_isbn_num_1.values.tolist()                            # converting the dataframe to list
                                    previous_isbn_num_1 = [item for sublist in previous_isbn_num_1 for item in sublist ]      #reitering the convertion from dataframe to list
                                else:
                                    previous_isbn_num_1 = ["-","-"]
        ###############################################################################################################################################################################################
        ###############################################################################################################################################################################################
                            temp_meta = GG.filter(items=['ISBN','US_PUB_DATE','PMG','PMC','Medium','TITLE_DISC','AUTHOR']) #filtering the variable GG with the column for meta data
                            str1 = temp_meta.values.tolist()                            # converting the dataframe to list
                            str1 = [item for sublist in str1 for item in sublist ]      #reitering the convertion from dataframe to list
                            # writing the HTML tags for metadata table. and assining the values from str1 variable 
                            if (j == 0) or (check_linn !=1):
                                str_html_temp ="""<table class= "table table-bordered"><thead> <th class="col-sm-2" style="background-color:lightgrey;"> ISBN (0)</th> <td class="col-sm-2">"""+ str(str1[0]) +"""</td><th class="col-sm-2" style="background-color:lightgrey;"> PMG</th> <td class="col-sm-2">""" + str(str1[2])+ """</td><tr><th class="col-sm-2" style="background-color:lightgrey;"> Pub Date</th> <td class="col-sm-2">""" + str(str1[1]) +"""</td><th class="col-sm-2" style="background-color:lightgrey;"> PMC</th> <td class="col-sm-2">""" + str(str1[3]) + """</td></tr><tr><th class="col-sm-2" style="background-color:lightgrey;"> Medium</th> <td class="col-sm-2">""" + str(str1[4]) + """</td><th class="col-sm-2" style="background-color:lightgrey;"> Author</th> <td class="col-sm-2">""" + str(str1[6]) + """</td></tr><tr><th class="col-sm-2" style="background-color:lightgrey;">Title</th><td class="col-sm-2">""" + str(str1[5]) + """</td></tr><tr><th class="col-sm-2" style="background-color:lightgrey;">Previous ISBN(-1)<td class="col-sm-2">""" + str(previous_isbn_num[0]) + """</td><th class="col-sm-2" style="background-color:lightgrey;">Pub Date:<td class="col-sm-2">""" + str(previous_isbn_num[1]) + """</td></tr><tr><th class="col-sm-2" style="background-color:lightgrey;">Previous ISBN(-2)<td class="col-sm-2">""" + str(previous_isbn_num_1[0]) + """</td><th class="col-sm-2" style="background-color:lightgrey;">Pub Date:<td class="col-sm-2">""" + str(previous_isbn_num_1[1]) + """</td></tr></table><tr><form action="post" onchange="this.value;"><td><div class="container"><div class="row"><div class="col-xs-12">"""
                                #print(j,GG)
                                if check_linn !=1 and warehouses[j] == "R" and check_linn <2:
                                    str_html_temp +="""<input type="radio" name="warehouse" data-toggle="collapse" data-target=".collapse""" + str(k) + """L ,.collapse"""+ str(k) + """R "/> Rushden  </td></form></tr>"""
                                    # writing the HTML tages to ISBN2 file, these html tags are for meta data, with collapsable window
                                    myfile.write("""<h4><p>MetaData</p></h4>""" +str_html_temp + """ """)
                                    #print(check_linn)
                                elif check_linn ==1 and warehouses[j] == "L":
                                    str_html_temp +="""<input type="radio" name="warehouse" data-toggle="collapse" data-target=".collapse""" + str(k) + """L ,.collapse"""+ str(k) + """R "/>  Linn  </td><td></form></tr><input type="radio" name="warehouse" data-toggle="collapse" data-target=".collapse""" + str(k) + """L ,.collapse"""+ str(k) + """R "/> Rushden  </td><td><input type="radio" name="warehouse" data-toggle="collapse" data-target=".collapse""" + str(k) + """BOTH">Combined</td></form></tr>"""
                                    # writing the HTML tages to ISBN2 file, these html tags are for meta data, with collapsable window
                                    myfile.write("""<h4><p>MetaData</p></h4>""" +str_html_temp + """ """)            
                                    check_linn = check_linn +1 
                            # writing the HTML tages to ISBN2 file, this sets up the table for current edition sales data
                            myfile.write(str_Html_L_R)
                            k = j - 1
                            if (not GG1.empty) & (warehouses[j]=="L"):
                                myfile.write("""<div>{% block test_to_extend_1 %}{% include "blog/ISBN1.html" %}{% endblock %}</div>""")
                            if (not GG2.empty) & (warehouses[j]=="L"):
                                myfile.write(""" <div>{% block test_to_extend_0 %}{% include "blog/ISBN0.html" %}{% endblock %}</div>""")
                            GG1 = []
                            GG2 = []
                        elif z == 0:
                            myfile.write("""<style>.alert { padding: 20px;   background-color: #f44336;    color: white;}.closebtn {margin-left: 15px;color: white;    font-weight: bold;    float: right;    font-size: 22px;    line-height: 20px;    cursor: pointer;   ransition: 0.3s;}.closebtn:hover {    color: black;}</style></head><body><div class="alert">  <span class="closebtn" onclick="this.parentElement.style.display='none';">&times;</span>   <strong>ISBN missing in database:  </strong>The ISBN """ + username + """ is not in the database. Please search a different ISBN</div></body>{% endblock content %}""")
                myfile.write("""</div></div></div></div></div></tr>{% endblock content %}""")
                myfile.close()
                
        return render(request, 'blog/ISBN2.html', )
            #return render(request, 'blog/test_to_extend.html')


def person_list(request):
    table = PersonTable(Person.objects.all())
    RequestConfig(request).configure(table)
    return render(request, 'blog/person_list.html', {'table': table})


def chart(request):
    bar_chart = pygal.Bar(fill=True, style=BlueStyle)  # Then create a bar graph object
    bar_chart.add('blue', [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55])  # Add some values
    chart = bar_chart.render_django_response()  # Save the svg to a file
    return render(request, 'svg/bar_chart.SVG', {'chart': chart}, content_type='image/svg+xml')

def test(a,Ed,edition_curr_prev,L_R):
    GG = a
    temp_meta = GG.filter(items=['ISBN','US_PUB_DATE','PMG','PMC','Medium','TITLE_DISC','AUTHOR']) #filtering the variable GG with the column for meta data
    str1 = temp_meta.values.tolist()                            # converting the dataframe to list
    str1 = [item for sublist in str1 for item in sublist ]      #reitering the convertion from dataframe to list
    # writing the HTML tages to ISBN2 file, these html tags are for meta data, with collapsable window
    str_html_previous = ""
    if L_R == "L":
        str_html_previous = ("""<div class="panel panel-default"><div class="panel-heading"><h4 class="panel-title"><a data-toggle="collapse" href="#collapse""" + str(Ed) + L_R + """"> """+ edition_curr_prev  +"""</a></h4></div><div id="collapse""" + str(Ed) + L_R + """" class="collapse"""+ str(Ed) + L_R +""" panel-collapse collapse in">""")
    else:
        str_html_previous = ("""<div id="collapse""" + str(Ed) + L_R + """" class="collapse"""+ str(Ed) + L_R +""" panel-collapse collapse">""")

    str_html_previous += (""" <div class="panel-body"><br/><div class="bs-example" data-example-id="table table-bordered" id ="table table-bordered"><table class= "table table-bordered"> <thead> <th class=""col-md-1"">""" + "Year" + """</th><th class=""col-md-1"">Jan</th> <th>Feb</th> <th>Mar</th> <th>Apr</th> <th>May</th> <th>Jun</th> <th>Jul</th> <th>Aug</th> <th>Sep</th> <th>Oct</th> <th>Nov</th> <th>Dec</th></tr> </thead> <tbody> <tr> """)
    lista = GG.filter(regex=("Period :*"))                       # using regex, getting all period sales
    lista = lista.values.tolist()                               # removing the headers from the dataframe
    lista = [item for sublist in lista for item in sublist ]    # converting dataframe to list
    lista = list(map(int, lista))                               # converting the list variables to integer
    max_num = max(list(map(int, lista)))                        # getting the max number for future use
    listb = GG.loc[:,'Month']                                   # taking only the month from the list row
    listc = GG.loc[:,'First Sale Month']                        #taking the first sale month for preparing the table
    listc=''.join((listc.tolist()))
    date1 = "1/" + listc[0:8]                                               # this is used for creating a running date period for sales table[]
    listc = listc.split("/")
    listc = int(listc[1])
    listb = listb.get_value(listb.index[0])                     # getting the month value
    str_html_previous += ("<td>" + str(listc) + "</td>")                      # writing the year to the ISBN2 file
    # if the first sale month is january then the below set of the codes works
    if int(listb) != 1:                     #condintion to check the first sale month equal to 1
        for i in range(0, listb):           # is the title doesnt have a sales start month as 1 then its pushed here
            lista.insert(0, 0)              # 0's are inserted based the month number
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
            str_html_previous += (str1 + "</tr>")# writing the str1 list to ISBN2 file
            #myfile.write
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
            str_html_previous += (listd + str1 + "</tr>")            #wRITING THE tags to the ISBN2 file
            #myfile.write
            a = a + 12
            listc = int(listc) 
            listc = listc + 1
            #print(listc)
    date2 = datetime.strptime(str(int(listc) + 1) + "-1-01", "%Y-%m-%d") # date2 variable to capture the last year
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
    output_file("U:\\django_test\\mysitetest\\blog\\templates\\svg\\bar"+ str(Ed)+ L_R +".svg")
    p = figure(plot_width=1500, title=L_R +'- (' +  edition_curr_prev +')', tools="",
               x_range=source.data["weight"],
               y_range=ranges.Range1d(start=0, end=(max_num + 100)), toolbar_location=None)
    p.line(months, Part_for_chart, line_width=2)
    labels = LabelSet(x='weight', y='height', text='height', level='glyph', x_offset=-13.5,
                      y_offset=0, source=source, text_font_size="10pt", render_mode='canvas')
    p.xaxis.major_label_orientation = math.pi / 2
    p.add_layout(labels)
    save(p)
    #show(p)
    #str_html_previous += ("""<table class="inlineTable"><div id="chart" >{% include "svg/bar"""+ str(Ed) + L_R +""".svg" %}</div></table><div class="col-md-9"></div></div></div></div></div></div>""")
    #str_html_previous += ("""<table class="inlineTable"><div id="chart" >{% include "svg/bar"""+ str(Ed) + L_R +""".svg" %}</div></table><div class="col-md-9"></div></div></div></div>""")
    str_html_previous += ("""<table class="inlineTable"><div id="chart" ><svg viewBox="0 0 60 55" width="100" height="50"><use xlink:href=""svg/bar"""+ str(Ed) + L_R +""".svg""/>    </svg></div></table><div class="col-md-9"></div></div></div></div>""")
    

    str_html_previous += ("</tr>")  
    return str_html_previous

def Linn_Rushden(dataDUMP, L_R,username,i):
    df = dataDUMP
    edition = i
    username = int(username)
    if (L_R == 'BOTH'):
        print(df.shape)
        booleans = []
        GG_combined = df.groupby(['ISBN']).get_group(username)
        for length in GG_combined['SUPPLY SITE']:
            if length == "L":
                booleans.append(True)
            else:
                booleans.append(False)

        GG_R = df[(df['ISBN'] == username) & (df['SUPPLY SITE'] == 'R')]                     #searching the ISBN in the dataframe
        GG_L = df[(df['ISBN'] == username) & (df['SUPPLY SITE'] == 'L')]                     #searching the ISBN in the dataframe
        GG_combined = GG_combined.reset_index()
        F_S_M = GG_combined.loc[:,'SUPPLY SITE':'First Sale Month']  #F_S_M means First_sale_month
        Column_header = list(GG_L.columns.values)   #getting only the headers here
        F_S_M_Linn = F_S_M[(F_S_M['SUPPLY SITE']=="L")]
        F_S_M_Rush = F_S_M[(F_S_M['SUPPLY SITE']=="R")]
        list_temp_L = F_S_M_Linn.filter(items = ['First Sale Month'])
        list_temp_R = F_S_M_Rush.filter(items = ['First Sale Month'])
        list_temp_L = list_temp_L.values.tolist()                            # converting the dataframe to list
        list_temp_R = list_temp_R.values.tolist()                            # converting the dataframe to list
        list_temp_L = [item for sublist in list_temp_L for item in sublist ]      #reitering the convertion from dataframe to list 
        list_temp_R = [item for sublist in list_temp_R for item in sublist ]      #reitering the convertion from dataframe to list 
        #print(list_temp_L,list_temp_R)
#########################################################################################################################################################################################################################
#########################################################################################################################################################################################################################
##################In the below IF condition, the date fields for Linn and Rushden are received and checked whether it exist. if any of them doesnt exist, the below condtion will not work
##################The below set of codes are for summing linn and rushden sales data based on the first sales month.
#########################################################################################################################################################################################################################
#########################################################################################################################################################################################################################
        if list_temp_L and list_temp_R:
            list_temp_L = (list_temp_L[0]).split("/")
            list_temp_R = (list_temp_R[0]).split("/")
            if int(list_temp_L[1]) >= int(list_temp_R[1]):
                GG_combined_T = GG_combined[(GG_combined['SUPPLY SITE']=="L")]
                GG_combined_T = GG_combined_T.filter(regex=("Period : *"))
                GG_combined_T_0 = GG_combined_T.T
                temp_year = list_temp_L[1]
                temp_year = int(temp_year) - int(list_temp_R[1]) 
                temp_year = int(temp_year)
                j = temp_year*12
                if int(list_temp_L[0])!= 1:
                    temp = list_temp_L[0]
                    temp = 12 - int(temp)
                    temp = int(temp)
                    #print(temp)
                    j = j + temp
                GG_combined_T=(GG_combined_T_0.shift(j)).T
                L = "R"
            elif int(list_temp_L[1]) < int(list_temp_R[1]):
                GG_combined_T = GG_combined[(GG_combined['SUPPLY SITE']=="R")]
                GG_combined_T = GG_combined_T.filter(regex=("Period : *"))
                GG_combined_T_1 = GG_combined_T.T
                temp_year = list_temp_R[1]
                temp_year = int(temp_year) - int(list_temp_L[1]) 
                temp_year = int(temp_year)
                j = temp_year*12
                if int(list_temp_R[0])!= 1:
                    temp = list_temp_R[0]
                    temp = 12 - int(temp)
                    temp = int(temp)
                    j = j + temp
                GG_combined_T=(GG_combined_T_1.shift(j)).T
                L = "L"
            if L == "R":
                GG_A = GG_R.filter(items=['PIN','ISBN','PMG','PMC','Medium','Extended Medium','AREA_OF_ACTIVITY','PRODUCT_OWNERSHIP','TITLE_DISC','AUTHOR','PACK_TYPE','DIVISION','Previous EDITION(-1)','Previous EDITION(-2)','US_PUB_DATE','UK_PUB_DATE','SUPPLY SITE','First Sale Month','End Sale Month','Month','Quarter','Sale Period(in Months)','First Year Sales','Second Year Sales','Third Year Sales','Fourth Year Sales','Fifth Year Sales','Range Sales Cluster','Previous Edition Cluster','Cluster : 2-12','Cluster : 1-12','Cluster : 13-24','Cluster : 25-36','Cluster : 37-48','Cluster : 49-60','Cluster : 1-24','Cluster : 1-36','Cluster : 1-48','Cluster : 1-60'])
                GG_R =  GG_R.filter(regex=("Period :*"))
                #print(GG_combined_T)
                GG_combined = GG_combined_T.add(GG_R,fill_value=0)
                GG_combined = GG_combined.reset_index()
                GG_combined_T = pd.DataFrame(GG_combined.sum(axis=0))
                GG_combined = GG_combined_T.T
                #print(GG_combined)
            elif L == "L":
                GG_A = GG_L.filter(items=['PIN','ISBN','PMG','PMC','Medium','Extended Medium','AREA_OF_ACTIVITY','PRODUCT_OWNERSHIP','TITLE_DISC','AUTHOR','PACK_TYPE','DIVISION','Previous EDITION(-1)','Previous EDITION(-2)','US_PUB_DATE','UK_PUB_DATE','SUPPLY SITE','First Sale Month','End Sale Month','Month','Quarter','Sale Period(in Months)','First Year Sales','Second Year Sales','Third Year Sales','Fourth Year Sales','Fifth Year Sales','Range Sales Cluster','Previous Edition Cluster','Cluster : 2-12','Cluster : 1-12','Cluster : 13-24','Cluster : 25-36','Cluster : 37-48','Cluster : 49-60','Cluster : 1-24','Cluster : 1-36','Cluster : 1-48','Cluster : 1-60'])
                GG_L =  GG_L.filter(regex=("Period :*"))
                #print(GG_combined_T)
                GG_combined = GG_combined_T.add(GG_L,fill_value=0)
                #GG_combined = GG_combined.T
                #print(GG_combined)

            GG_combined = GG_combined.reset_index()
            GG_combined = GG_combined.drop('index',1)
            GG_A = GG_A.reset_index()
            GG_combined = pd.concat([GG_combined, GG_A], axis=1)
        elif list_temp_L:
            GG_combined = GG_L
            #print(GG_combined)
        elif list_temp_R:
            GG_combined = GG_R
            #print(GG_combined)
        else:
            GG_combined = {}
#########################################################################################################################################################################################################################
#########################################################################################################################################################################################################################
#########################################################################################################################################################################################################################
#########################################################################################################################################################################################################################

        if not GG_combined.empty:
            str_Html = test(GG_combined,edition,"Current Edition",L_R)
            #print(GG_combined)
            #print(str_Html)
            return str_Html,GG_combined
    elif L_R == 'L' or L_R == 'R':
        GG = df[(df['ISBN'] == int(username)) & (df['SUPPLY SITE'] == (L_R.strip(" ")))]                     #searching the ISBN in the dataframe
        if not GG.empty:
            str_Html = test(GG,edition,"Current Edition ",L_R)
            return str_Html,GG
        else:
            str_Html = ""
            GG = pd.DataFrame({'a':[] })
            return str_Html,GG
            
