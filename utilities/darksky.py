#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 15 09:26:25 2020

@author: michaelkarachewski

Takes rows of (lon,lat,date) inputs from a CSV and calls DarkSky Weather API
several times for each entry to output 13 weather features and other fields to a CSV.

Can take additional inputs for speeding up or breaking apart lookup tasks
"""

import requests
import json
import time
import csv
import datetime
from datetime import datetime,timedelta
from collections import namedtuple
import argparse
import os
  
# api-endpoint 

#s = "01/12/2011"
#start_date = "01/12/2011"




def create_input_vector(start_date, lat, long, label, idnum, write_file_list):
    print(str(start_date))
    date_time=time.mktime(datetime.strptime(start_date, "%Y/%m/%d").timetuple())
    time_str=str(int(date_time))  
    lat=str(lat)
    long=str(long)
    #lat=str(37.8267)
    #long=str(-122.4233)
    print(lat,long,time_str)
    input_str="https://api.darksky.net/forecast/a749d1757a59ffb0be2d82fbdd7794f5/"+lat+","+long+","+time_str+"?exclude=hourly"
    print(input_str)
    response=requests.get(input_str)
    json_response=response.json()
    #print(json_response["hourly"])
    
    
     
    seven_day_rainfall_average=0
    three_day_rainfall_average=0
    temp_high_0=0
    temp_high_1=0
    temp_high_2=0
    temp_low_0=0
    temp_low_1=0
    temp_low_2=0
    humidity_0=0
    humidity_1=0
    humidity_2=0
    cloud_cover_day_of=0
    wind_speed_day_of=0
    
    x=1
    while(x<=7):
        dt=datetime.strptime(start_date, "%Y/%m/%d")
        d = dt - timedelta(days=x)
        date_time=time.mktime(d.timetuple())
        date_time_str=str(int(date_time))
        input_str="https://api.darksky.net/forecast/a749d1757a59ffb0be2d82fbdd7794f5/"+lat+","+long+","+date_time_str+"?exclude=hourly"
        response=requests.get(input_str)
        json_response=response.json()
        data_object=json_response["daily"]
        data_object=data_object["data"][0]

        ## Calculated values from dataset for filling in bad queries
        seven_day_rainfall_avg_GLOBAL = 0.004205333333 
        # three_day_rainfall_avg_GLOBAL = 0.001785238095
        temp_high_avg_GLOBAL = [86.97478095, 86.55757778, 86.50067302]
        temp_low_avg_GLOBAL =  [58.4750127, 58.48488254, 57.99777143]
        humidity_avg_GLOBAL = [0.3529047619, 0.3555174603, 0.358]
        cloud_cover_avg_GLOBAL = 0.1298126984
        wind_speed_avg_GLOBAL = 5.461990476
        
        try:
            temphigh=data_object["temperatureHigh"]
        except KeyError:
            if (x < 4):
                temphigh = temp_high_avg_GLOBAL[x-1]
            else:
                temphigh = temp_high_avg_GLOBAL[2]

        try:
            templow=data_object["temperatureLow"]
        except KeyError:
            if (x<4):
                templow = temp_low_avg_GLOBAL[x-1]
            else:
                templow = temp_low_avg_GLOBAL[2]

        try:
            rainfall=data_object["precipIntensity"]
        except KeyError:
            rainfall = seven_day_rainfall_avg_GLOBAL/7

        try:
            humidity=data_object["humidity"]
        except:
            if (x<4):
                humidity = humidity_avg_GLOBAL[x-1]
            else:
                humidity = humidity_avg_GLOBAL[2]

        try:
            cloudcover=data_object["cloudCover"]
        except KeyError:
            cloudcover = cloud_cover_avg_GLOBAL
        
        try:
            windspeed=data_object["windSpeed"]
        except:
            windspeed = wind_speed_avg_GLOBAL


        seven_day_rainfall_average+=rainfall
        if(x<=3):
            three_day_rainfall_average+=rainfall
        
        if(x==1):
            temp_high_0=temphigh
            temp_low_0=templow
            humidity_0=humidity
            cloud_cover_day_of=cloudcover
            wind_speed_day_of=windspeed
        if(x==2):
            temp_high_1=temphigh
            temp_low_1=templow
            humidity_1=humidity
        if(x==3):
            temp_high_2=temphigh
            temp_low_2=templow
            humidity_2=humidity
            
       
            
        
        #print(temphigh,templow,rainfall,humidity,cloudcover,windspeed,windgust)
        x+=1
    
    
    fields=[]
    
    fields=[start_date,
            label,
            lat,
            long,
            idnum,
            seven_day_rainfall_average,
            three_day_rainfall_average,
            temp_high_0,
            temp_high_1,
            temp_high_2,
            temp_low_0,
            temp_low_1,
            temp_low_2,
            humidity_0,
            humidity_1,
            humidity_2,
            cloud_cover_day_of,
            wind_speed_day_of]
    write_file_list.append(fields)
    
        


if __name__ == "__main__":
    parser =argparse.ArgumentParser(description="Create training data. See --help for usage info")
    parser.add_argument("--S", type=int, default=0, help="ID of data to start collection on")
    parser.add_argument("--E", type=int, default=10, help="ID of data to end collection on")
    parser.add_argument("--skip_file", type=str, help="Name of csv file with id's already used, as to no repeat.")

    args = parser.parse_args()

    skip_ids = set()

    if (args.skip_file):
        with open(args.skip_file, 'r') as f:
            reader = csv.reader(f, delimiter=',')
            skip_ids = set([int(val[0]) for val in reader])
    
    dates=["06/12/2011",
            "06/12/2010",
            "06/12/2009",
            "06/12/2008",
            "06/12/2009"]
    
    coors=[[34.622102,-119.189236], 
                 [34.098835,-118.517032],
                 [33.485254,-117.553303],
                 [32.890705,-117.061493], 
                 [38.488095,-122.355208]]
    
    write_to_file=[]
    training_points=[]

    with open('fires.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        counter=0
        for row in spamreader:
            if (counter >= args.S):
                if counter>=args.E:
                    break

            
                year=row[0]
                label=row[1]
                latitude=row[2]
                longitude=row[3]
                idnum=row[4]
                '''index=row[0].find("[")
                year=row[0].split(",")[0]
                print(year)
                latlong=(row[0][index:])
                index2=latlong.find(",")
                index3=latlong.find("]")
                latitude=latlong[1:index2]
                print(latitude)
                longitude=latlong[index2+1:index3]
                print(longitude)
                label=row[0].split(",")[1]
                print(label)'''
                
                templist=[year,latitude,longitude,label,idnum]
                
                #temp=row[0].split(",")
                training_points.append(templist)
            counter+=1
    
    if (len(training_points)):
        training_points.pop(0)

    
    if os.path.exists("trainingdata.csv"):
        append_write = 'a' # append if already exists
    else:
        append_write = 'w' # make a new file if not
    
    fp = open("trainingdata.csv", append_write)
    writer = csv.writer(fp, quoting=csv.QUOTE_NONNUMERIC)
    counter = 0
    error_counter = 0
    for date, lat, lon, label, idnum in training_points:
        print("We are {:.1f}% done".format(100*counter/(args.E - args.S)))
        try:
            if int(idnum) not in skip_ids:
                create_input_vector(date, lat, lon, label, idnum, write_to_file)
                writer.writerow(write_to_file[-1])
            else:
                print("Already used ID, skipping")
        except KeyError:
            error_counter += 1
        counter += 1

    fp.close()

    print("{} errors occured during API calls".format(error_counter))
           
