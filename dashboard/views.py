from django.shortcuts import render
from django.http import JsonResponse
import os
import csv
import time
import datetime
from pprint import pprint
from dotenv import load_dotenv
# Create your views here.


def index(request):
    return render(request,'index.html')


def get_data_transaction(request):
    """
    Driver Code to get the data based on the drop down selected from 
    front end this function is called
    """

    load_dotenv()
    #environment path is received from the env config file
    directory_path = os.getenv("DIRECTORYPATH")
    file_path = directory_path+"/"+request.GET['filepath']
    file_header = {'chart_transactions.csv':'Transaction','live_data.csv':'Price','trends.csv':'Trend','live_tweet.csv':'Sentiment'}
    file_headkey = file_header.get(request.GET['filepath'])

    #from and to dates from datepicker
    if request.GET['from'] == ''  and request.GET['to'] =='': 
        csv_data_params = {"file_path":file_path,"file_headkey":file_headkey,"fromdate":request.GET['from'],"todate":request.GET['to']}
        # csv file reader function call
        data  = csv_file_reader(**csv_data_params) 
        return JsonResponse(data)
        
    else:
        fromdate = request.GET['from'].split(" ")[0]
        todate = request.GET['to'].split(" ")[0]
        csv_data_params = {"file_path":file_path,"file_headkey":file_headkey,"fromdate":fromdate,"todate":todate}
        # csv file reader function call
        data  = csv_file_reader(**csv_data_params)
        return JsonResponse(data)



def csv_file_reader(**csv_data):
    """ File reader function to read the file base on the drop down selected 
    from frontend 
    """

    datetime_converted = []
    sentiments_data = []
    with open(csv_data['file_path']) as csvfile:
            reader = csv.DictReader(csvfile)
            if csv_data['fromdate']=='' and csv_data['todate']=='':
                for i in reader:
                    #date conversion
                    converted_time = datetime.datetime.strptime(i['Time'], "%y-%m-%d-%H-%M").strftime("%d-%m-%Y %H:%M")
                    datetime_converted.append(converted_time)
                    sentiments_data.append(i[csv_data['file_headkey']])
            else:
                for i in reader:
                    #date conversion
                    converted_time = datetime.datetime.strptime(i['Time'], "%y-%m-%d-%H-%M").strftime("%d-%m-%Y")

                    #check for from and todate from csv with the datepicker
                    if datetime.datetime.strptime(converted_time,"%d-%m-%Y") >= datetime.datetime.strptime(csv_data['fromdate'],"%d-%m-%Y") and datetime.datetime.strptime(converted_time,"%d-%m-%Y") <= datetime.datetime.strptime(csv_data['todate'],"%d-%m-%Y"):
                        datetime_converted.append(converted_time)
                        sentiments_data.append(i[csv_data['file_headkey']])
    
    data = {
            'time':datetime_converted,
            'sentiments':sentiments_data
        }

    return data
