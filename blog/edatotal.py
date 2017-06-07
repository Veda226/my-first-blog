import pandas as pd
import numpy as np
from random import sample
import csv
import glob
import os
import csv


#from .views import mylist

def Command(mylist):
    """ Do your work here """
    #from itertools import izip_longest
    #category = input("Enter the category for EDA:")
    #category = "CS"                                          #hardcode (remove it for original code
    category = mylist
    #category = models.CharField(max_length=3)
    #path = input("Mention the path for category files : ")               #hardcode (remove it for original code)
    path = "C:\\Users\\prasadv\\Desktop\\Stock Opt\\Data Dump" 
    path = "".join(path)
    
    #path = models.CharField(max_length=200)
    path1=  os.path.join(path, "*"+category+"*.csv")   #for os independent directory traversal

    list_datafiles = glob.glob(path1)        #list all the files associated with that category

        # print list_datafiles
        # print len(list_datafiles)


    df = pd.concat((pd.read_csv(f,encoding='iso-8859-1') for f in list_datafiles))     #merges all the files of that category into one
    pd.set_option('display.max_columns', None)    #not required can ignore it

        # columnlist =  df.columns.values.tolist()
        # print "\n".join(columnlist)

        #pathSave = input("Enter the path where output will be saved : ")
    pathSave= "C:\\Users\\prasadv\\Desktop\\Stock Opt"            #hardcode (remove it for original code)
    pathSave = "".join(pathSave)

    df_data = df.describe(include='all')         #describes all the columns
    df_data = df_data.T                          #transpose
    file_out = df_data.to_csv(sep=',')           #csv format

    with open(os.path.join(pathSave,"Data.csv"),"w") as outfile:
        outfile.write(file_out)
        columnlist =['Doc Type (Code)','Doc Type (Desc)','Customer Account','Send-to Customer Name','Supply Site (Code)','Transaction Type (Code)','Transaction Type (Desc)','Pack Type (Code)','Pack Type (Desc)','PMG (Code)','PMG (Desc)','PMC (Code)','PMC (Desc)','Sbu','Sbu Group','Customer Type (Code)','Customer Type (Desc)','Product Ownership (Code)','Product Ownership (Desc)','Medium (Code)','Medium (Desc)','Edition Type (Code)','Edition Type (Desc)','Extended Medium (Code)','Extended Medium (Desc)','Product Type (Code)','Product Type (Desc)','Answer Code (Code)','Answer Code (Desc)']                #the desired columns for which we need to find unique values
        final_list = []
        i=0

    
    for columnName in columnlist:
        temp =df[columnName].unique()
        final_list.append(temp)       #list of unique values unique values of all columns
        i += 1
    del list_datafiles
    #columnlist
    del final_list
    del df_data
    del file_out
    del temp
    with open(os.path.join(pathSave,"Uniques.csv"),"w") as f:
        writer = csv.DictWriter(f, fieldnames=columnlist, delimiter=',')
        writer.writeheader()
        writer = csv.writer(f)

    #for values in izip_longest(*final_list):
        #writer.writerow(values)
        #======================various correaltions with frequency,total.min,max for each of them===========================
    #df_docType = df[['Doc Type (Code)','Doc Type (Desc)', 'Delivered Qty']].groupby(['Doc Type (Code)','Doc Type (Desc)']).agg(['sum', 'count','max','min'])
    df_PMG = df[['PMG (Code)','PMG (Desc)', 'Delivered Qty']].groupby(['PMG (Code)','PMG (Desc)']).agg(['sum', 'count','max','min'])
    f_PMG = df_PMG.to_csv(sep=',')
    with open(os.path.join(pathSave,"PMG_Types.csv"), "w") as output:
        output.write(f_PMG)
    with open(os.path.join(pathSave,"Doc_Types.csv"), "w") as output:
        output.write(f_PMG)

    df_PMC = df[['PMC (Code)','PMC (Desc)', 'Delivered Qty']].groupby(['PMC (Code)','PMC (Desc)']).agg(['sum', 'count','max','min'])
    df_supply = df[['Supply Site (Code)', 'Delivered Qty']].groupby(['Supply Site (Code)']).agg(['sum', 'count','max','min'])
    df_transaction = df[['Transaction Type (Code)','Transaction Type (Desc)', 'Delivered Qty']].groupby(['Transaction Type (Code)','Transaction Type (Desc)']).agg(['sum', 'count','max','min'])
    df_sbu = df[['Sbu', 'Delivered Qty']].groupby(['Sbu']).agg(['sum', 'count','max','min'])
    df_edition = df[['Edition Type (Code)','Edition Type (Desc)', 'Delivered Qty']].groupby(['Edition Type (Code)','Edition Type (Desc)']).agg(['sum', 'count','max','min'])
    df_medium = df[['Medium (Code)','Medium (Desc)','Extended Medium (Code)','Extended Medium (Desc)','Delivered Qty']].groupby(['Medium (Code)','Medium (Desc)','Extended Medium (Code)','Extended Medium (Desc)']).agg(['sum', 'count','max','min'])
    df_PMG_PMC = df[['PMG (Code)','PMG (Desc)','PMC (Code)','PMC (Desc)', 'Delivered Qty']].groupby(['PMG (Code)','PMG (Desc)','PMC (Code)','PMC (Desc)']).agg(['sum', 'count','max','min'])
    df_customer = df[['Customer Type (Code)','Customer Type (Desc)','Customer Account','Send-to Customer Name', 'Delivered Qty']].groupby(['Customer Type (Code)','Customer Type (Desc)','Customer Account','Send-to Customer Name']).agg(['sum', 'count','max','min'])
    #f_docType = df_docType.to_csv(sep=',')

    f_PMC = df_PMC.to_csv(sep=',')
    f_supply = df_supply.to_csv(sep=',')
    f_transaction= df_transaction.to_csv(sep=',')
    f_sbu = df_sbu.to_csv(sep=',')
    f_edition = df_edition.to_csv(sep=',')
    f_medium = df_medium.to_csv(sep=',')
    f_PMG_PMC = df_PMG_PMC.to_csv(sep=',')
    f_customer = df_customer.to_csv(sep=',')

    #self.stdout.write('There are {} things!'.format(MyModel.objects.count()))
    
    with open(os.path.join(pathSave,"Supply_Site.csv"), "w") as output:
        output.write(f_supply)
    with open(os.path.join(pathSave,"Transcation_Types.csv"), "w") as output:
        output.write(f_transaction)
    with open(os.path.join(pathSave,"SBU.csv"), "w") as output:
        output.write(f_sbu)
    with open(os.path.join(pathSave,"Edition_Types.csv"), "w") as output:
        output.write(f_edition)
    with open(os.path.join(pathSave,"Medium_with_ExtendedMedium_Types.csv"), "w") as output:
        output.write(f_medium)
    with open(os.path.join(pathSave,"PMG_PMC(subcat).csv"), "w") as output:
        output.write(f_PMG_PMC)
    with open(os.path.join(pathSave,"CustomerSales.csv"), "w") as output:
        f_customer=str(f_customer.encode('utf-8'))
        output.write(f_customer)
    with open(os.path.join(path,"PMC_Types.csv"), "w") as output:
        output.write(f_PMC)











# =======================List of columns==================
# Doc Ref (Invoice Number)
# Doc Type (Code)
# Doc Type (Desc)
    # Doc Date
    # ISBN13
    # Customer Account
    # Send-to Customer Name
    # Delivered Qty
    # Shipped Date
    # Supply Site (Code)
    # Transaction Type (Code)
    # Transaction Type (Desc)
    # OpCo (Code)
    # OpCo (Desc)
    # Pack Type (Code)
    # Pack Type (Desc)
    # Published Date
    # PMG (Code)
    # PMG (Desc)
    # PMC (Code)
    # PMC (Desc)
    # Customer Discount (Code)
    # Sbu
    # Sbu Group
    # Customer Type (Code)
    # Customer Type (Desc)
    # Isbn13 (Previous)
    # Title
    # Author
    # HS/S&T (Code)
    # HS/S&T (Desc)
    # Title Disc Desc
    # Title Disc
    # Product Ownership (Code)
    # Product Ownership (Desc)
    # Medium (Code)
    # Medium (Desc)
    # Edition Type (Code)
    # Edition Type (Desc)
    # Extended Medium (Code)
    # Extended Medium (Desc)
    # Product Type (Code)
    # Product Type (Desc)
    # Answer Code (Code)
    # Answer Code (Desc)
    # =======================List of columns==================

