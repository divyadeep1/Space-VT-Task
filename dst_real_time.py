# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 14:58:36 2018

@author: divyadeep
"""

#Scrape data from website "wdc.kugi.kyoto-u.ac.jp/dst_realtime/{year-month}"

from bs4 import BeautifulSoup as bs
import urllib.request
import sqlite3

def correct(data):
	#Function to split values in list 'data' that contain data of more than
	#hour (Example : '-111-121')
	#
	#Arguement:
	#    data: list: list containing hourly dst value where one or more are
	#        merged into a single index.
	#
	#Returns:
	#    data: list: corrected list containing exactly 25 values.
    while(len(data)!=25):
        for i in data[1:]:
            if(len(i)>4):
                breaker = i.index('-', 1)
                t1 = i[:breaker]
                t2 = i[breaker:]
                index = data.index(i)
                data.remove(i)
                data.insert(index, t2)
                data.insert(index, t1)
    return data

#Basic definitions.
base_url = "http://wdc.kugi.kyoto-u.ac.jp/dst_realtime/"
years = [2016, 2017]
months = ['01','02','03','04','05','06','07','08','09','10','11','12']

#Creating the table.
conn = sqlite3.connect('dst.db')
cur = conn.cursor()
cur.execute("CREATE TABLE dst_realtime (Year integer, Month integer, Day integer)")
for hour in range(1,25):
    cur.execute("ALTER TABLE dst_realtime ADD COLUMN Hour_{} integer".format(hour))

#Opening web pages monthwise and writing their daily dst index data to the database.
for year in years:
    for month in months:
        print("Executing for {},{}".format(month, year))
        url = base_url + '{}{}/'.format(year, month)
        html_doc = urllib.request.urlopen(url).read()
        raw_data = bs(html_doc, 'html.parser').pre.get_text().split('\n')[8:-2] #Splitting the obtained data to make it contain only the dst values (observed from page source)
        for line in raw_data:
            if len(line) > 10: #'raw_data' contains empty lines as well, here we are skipping them. ('10' is arbitrary)
                data = line.split()
                if len(data)!=25: #If 'data' doesn't contain exactly 25 values (1 value depicting the day and the rest 24 values corresponding to 24 hours), then data needs to be corrected.
                    data = correct(data)
                data.insert(0, months.index(month)+1)
                data.insert(0, year) #Inserting month and year to the list 'data'.
                cur.execute("""INSERT INTO dst_realtime VALUES (?,?,?,?,?,?,?,?,
                ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", data) #Inserting values to the data base
        conn.commit()
        print("Data for {}, {} successfully written to the database".format(month, year))

#The next section (till line 86) is for the year 2018 as the complete data for this year isn't available currently.
#Once data for a particular month is available completely, the month can be added to the list in line number 72 to obtain data for that month.
#Once data for year 2018 is available, '2018', can be added to list 'years'.
year = 2018
for month in ['01']:
    print("Executing for {},{}".format(month, year))
    url = base_url + '{}{}/'.format(year, month)
    html_doc = urllib.request.urlopen(url).read()
    raw_data = bs(html_doc, 'html.parser').pre.get_text().split('\n')[8:-2]
    for line in raw_data:
        if len(line) > 10:
            data = line.split()
            if len(data)!=25:
                data = correct(data)
            data.insert(0, months.index(month)+1)
            data.insert(0, year)
            cur.execute("""INSERT INTO dst_realtime VALUES (?,?,?,?,?,?,?,?,
            ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", data)
    conn.commit()
    print("Data for {}, {} successfully written to the database".format(month, year))
conn.close()
