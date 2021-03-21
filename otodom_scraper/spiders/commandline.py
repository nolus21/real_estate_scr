# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 17:42:17 2021

@author: nowak
"""

from pathlib import WindowsPath
import subprocess as sp
import os
import sys
import requests
import json
from bs4 import BeautifulSoup
import pandas as pd
import unicodedata
import csv
import urllib3
from urllib.request import urlopen
from csv import writer
from csv import reader
import threading
from lxml import html
import re
import math
import threading

import glob



district = 'jezyce'
check = 'https://www.otodom.pl/sprzedaz/mieszkanie/poznan/' + district
git_bash_path = WindowsPath(r"C:\Program Files\Git\git-bash.exe")




number = []



def check_number_of_pages(check):
    

    
    #print(url)
    html = requests.get(check).content
    #print(html)
    soup= BeautifulSoup(html, 'html.parser')
    offers = [a.text.strip() for a in soup.select('.offers-index.pull-left.text-nowrap strong')]
    number.extend(offers)
    #print(soup.title.string)
    print(district + ' ' + offers[0] + ' oferty')
    print(number)
    
check_number_of_pages(check)


def spit_scraping_commands(number):

    print(float(number[0]))
    no_pages = float(number[0])/72
    print(no_pages)
    n = math.ceil(no_pages)
    print(n)
    
    
    for m in range(1,n+1):
        print(m)
        
    
        home_dir = os.system("cd C:/Users/nowak/otodom_scraper/otodom_scraper/spiders")
        bashCommand = "scrapy crawl crawl_ads_basic -o " + district + '_auto' + str(m) + '.csv' + ' -a locations=Poznan/' + district + ' -a' + ' ' + 'page=' + str(m)
        print(bashCommand)
    
        #output = sp.check_output(['bash','-c', bashCommand])
        output = os.system(bashCommand)
       
        print(output)
      
# =============================================================================
#         bashCommand = "scrapy crawl crawl_ads_basic -o " + 'lazarz_auto' + str(m) + '.csv' + ' -a locations=Poznan/' + district + ' -a' + ' ' + 'page=' + str(m)
#         print(bashCommand)
#     
#        # output = sp.check_output(['bash','-c', bashCommand])
#         output = sp.Popen(bashCommand.split(), cwd='C:/Users/nowak/otodom_scraper/otodom_scraper/spiders')
#         output.wait()
#         print(output)
# =============================================================================

spit_scraping_commands(number)
  



#   ------------------   THERE CANNOT BE ANY OTHER FILES IN THE FOLDER !!! ---------------------
def combine_csv():

    #Step 1: Import packages and set the working directory
    
    #os.chdir("/mydir")
    
    #Step 2: Use glob to match the pattern ‘csv’
    
    extension = 'csv'
    all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
    
    
    
    
    #Step 3: Combine all files in the list and export as CSV
    
    #combine all files in the list
    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
    #export to csv
    combined_csv.to_csv( district + '_' + "combined.csv", index=False, encoding='utf-8-sig')
    
    output_file_name = district + '_' + "combined.csv"
    print(output_file_name)
   

#delay = int(input("Enter the delay time :"))
delay = 2
start_time = threading.Timer(delay,combine_csv)
start_time.start()
print ("End of the code")






# =============================================================================
# 
# 
# 
# 
# 
# 
# 
# 
# input_file = final_file[0]
# output_file = 'xx.csv'
# # =============================================================================
# # def geocode():
# #     
# #         home_dir = os.system("cd C:/Users/nowak/otodom_scraper")
# #         bashCommand2 = "geocode_2021.py"
# #         print(bashCommand2)
# #     
# #         #output = sp.check_output(['bash','-c', bashCommand])
# #         output = os.system(bashCommand2)
# #        
# #         print(output)
# #         final_file.extend(output)
# # 
# # geocode()
# # 
# # #---------------------------------------------------------------------------------------------------------------
# # 
# # 
# # 
# # 
# # 
# # 
# # def remove_diacritics(input_str):
# #     nfkd_form = unicodedata.normalize('NFKD', input_str.replace('ł', 'l'))
# #     return u''.join([c for c in nfkd_form if not unicodedata.combining(c)])
# # # remove_diacritics('zażółć gęślą jaźń')
# # 
# # 
# # 
# # 
# # 
# # input_file = final_file[0]
# # output_file = 'happening.csv'
# # =============================================================================
# 
# 
# 
# 
# all_lat=[]
# all_lon=[]
# all_CONSTR_STAT=[]
# all_OWN=[]
# 
# #FUNCTION FOR LAT
# def add_column_LAT_in_csv(input_file, output_file, all_lat, all_lon):
#     
#     with open(input_file, encoding="utf8", newline='') as read_obj, \
#         open(output_file, 'w', newline='') as write_obj: #Optional for other type of code
#  
#         csv_reader = csv.DictReader(read_obj)
#         #csv_writer = writer(write_obj)
# 
#         
#         def add_LAT_LON():
#             for row in csv_reader:
#                 try:
#                     url = row['url']
#                     #print(url)
#                     html = requests.get(url).content
#                     soup= BeautifulSoup(html, 'html.parser')
#                     print (soup.title.string)
#                     
#                     script = soup.find_all('script', {'id': '__NEXT_DATA__'})
#                    
#                     #if e.g. the add is somehow outdated...
#                     if not script:
#                         
#                         all_lat.extend(['no_data'])
#                         all_lon.extend(['no_data'])
#                         
#                     #here add more...
#                         
#                     #print(script)
#                     section = script[0].text.strip() if script else 'Empty' # THIS PREVENTS LIST INDEX OUT OF RANGE - for some reason?
#                     #print(section)
#                     
#                     data_LAT = json.loads(section)
#                     data_LON = json.loads(section)
#                     
#                     json_LAT = json.dumps(data_LAT['props']['pageProps']['adTrackingData']['lat'])
#                     json_LON = json.dumps(data_LON['props']['pageProps']['adTrackingData']['long'])
#                     
#                     
#                     #print(json_LAT)
#                     
#                     all_lat.extend([json_LAT])  
#                     all_lon.extend([json_LON])  #notice difference EXTEND and APPEND
#                     
#                     
#                     print(all_lat)
#                     print(all_lon)
#                     #print(all_CONSTR_STAT)
#                     
#                 except KeyError:
#                     all_OWN.extend(['no data'])
#                     pass
#                     #print('ERROR ERROR ERROR')
#                 except ValueError:
#                     #raise JSONDecodeError("Expecting value", s, 'lol') from None
#                     all_OWN.extend(['json error'])
#                     pass
#         add_LAT_LON()
# 
#     
#   # Parse the success state
# add_column_LAT_in_csv(input_file, output_file, all_lat, all_lon)
# 
# 
#             
# 
#             
# df = pd.read_csv(input_file)
# for item in [all_lat]:
#     df["Lat"] = item
#     df.to_csv(input_file, index=False)
#     
# for item in [all_lon]:
#     df["Lon"] = item
#     df.to_csv(input_file, index=False)
# 
# 
# 
# 
# =============================================================================
