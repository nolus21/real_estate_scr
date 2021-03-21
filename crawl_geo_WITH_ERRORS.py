


# -*- coding: utf-8 -*-
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


def remove_diacritics(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str.replace('ł', 'l'))
    return u''.join([c for c in nfkd_form if not unicodedata.combining(c)])
# remove_diacritics('zażółć gęślą jaźń')

input_file = 'Wilda1.csv'
output_file = 'Wilda1_latlon.csv'


all_lat=[]
all_lon=[]
all_CONSTR_STAT=[]
all_OWN=[]

#FUNCTION FOR LAT
def add_column_LAT_in_csv(input_file, output_file, all_lat, all_lon):
    
    with open(input_file, encoding="utf8", newline='') as read_obj, \
        open(output_file, 'w', newline='') as write_obj: #Optional for other type of code
 
        csv_reader = csv.DictReader(read_obj)
        #csv_writer = writer(write_obj)

        
        for row in csv_reader:
            try:
                url = row['url']
                #print(url)
                html = requests.get(url).content
                soup= BeautifulSoup(html, 'html.parser')
                print (soup.title.string)
                
                script = soup.find_all('script', {'id': '__NEXT_DATA__'})
               
                #if e.g. the add is somehow outdated...
                if not script:
                    
                    all_lat.extend(['no_data'])
                    all_lon.extend(['no_data'])
                    
                #here add more...
                    
                #print(script)
                section = script[0].text.strip() if script else 'Empty' # THIS PREVENTS LIST INDEX OUT OF RANGE - for some reason?
                #print(section)
                
                
# =============================================================================
#         #Construction status 
#                 data_CONSTR_STAT = json.loads(section)
#                 json_CONSTR_STAT = json.dumps(data_CONSTR_STAT['initialProps']['meta']['target']['Construction_status'])
#                 all_CONSTR_STAT.extend([json_CONSTR_STAT]) #notice difference EXTEND and APPEND
#                 print(all_CONSTR_STAT)
# =============================================================================
                
                
                
                data_LAT = json.loads(section)
                data_LON = json.loads(section)
                
                json_LAT = json.dumps(data_LAT['props']['pageProps']['adTrackingData']['lat'])
                json_LON = json.dumps(data_LON['props']['pageProps']['adTrackingData']['long'])
                
                
                #print(json_LAT)
                
                all_lat.extend([json_LAT])  
                all_lon.extend([json_LON])  #notice difference EXTEND and APPEND
                
                
                print(all_lat)
                print(all_lon)
                #print(all_CONSTR_STAT)
                
            except KeyError:
                all_OWN.extend(['no data'])
                pass
                #print('ERROR ERROR ERROR')
            except ValueError:
                #raise JSONDecodeError("Expecting value", s, 'lol') from None
                all_OWN.extend(['json error'])
                pass
                
                
                
# =============================================================================
#         #Ownership
#                 data_OWN = json.loads(section)
#                 print(data_OWN)
#                 json_OWN = json.dumps(data_OWN['initialProps']['meta']['target']['Building_ownership'])
#                 all_OWN.extend([json_OWN]) #notice difference EXTEND and APPEND
#                 print(all_OWN)
#                 
#             except KeyError:
#                 all_OWN.extend(['no data'])
#                 pass
#                 #print('ERROR ERROR ERROR')
#             
# # =============================================================================
# #             except KeyError:
# #                 all_CONSTR_STAT.extend(['no data'])
# #                 pass
# #                 #print('ERROR ERROR ERROR')
# #             
# # =============================================================================
#             except ValueError:
#                 #raise JSONDecodeError("Expecting value", s, 'lol') from None
#                 all_OWN.extend(['json error'])
#                 pass
# =============================================================================
            
# =============================================================================
#             except ValueError:
#                 #raise JSONDecodeError("Expecting value", s, 'lol') from None
#                 all_CONSTR_STAT.extend(['json error'])
#                 pass
# =============================================================================
                    
                
            #all_OWN.extend([json_OWN]) #notice difference EXTEND and APPEND
            
            #print(all_OWN)

    
  # Parse the success state
add_column_LAT_in_csv(input_file, output_file, all_lat, all_lon)
#add_column_LON_in_csv(input_file, output_file, all_lon)

            

            
df = pd.read_csv(input_file)
for item in [all_lat]:
    df["Lat"] = item
    df.to_csv(input_file, index=False)
    
for item in [all_lon]:
    df["Lon"] = item
    df.to_csv(input_file, index=False)
    
# =============================================================================
# for item in [all_CONSTR_STAT]:
#     df["Const_Stat"] = item
#     df.to_csv(input_file, index=False)
# =============================================================================
# =============================================================================
#     
# for item in [all_OWN]:
#     df["ownership"] = item
#     df.to_csv(input_file, index=False)
# =============================================================================

    
    
          
                

           
           
           
           
        
    
#split_csv = csv_raw_cont.split('\n')
#split_csv.remove('')
#separator=","

#next(split_csv)
#for each in split_csv[1:]:
    
#    url_row_index=12
    
    
    
 
    
    
    #for row in reader:
        #all_urls.append(row[12])
        


#name = 'crawl_geo'
#allowed_domains = ['otodom.pl']
#print(name)


#url = 'https://www.otodom.pl/oferta/-' + 'ID46zgs'
#print(url)

#print(requests.get(url).text)

#r = requests.get(url)
#soup = BeautifulSoup(r.content, 'html.parser')
#script = soup.find_all('script', {'id': 'server-app-state'})[0].text.strip()
#print(script)
#CHECK IN JSONFORMATTER.ORG if the result till now is a valid JSON
# get data mised double and single quotes

#data_sQUOTES = json.loads(script)
#print(data)
#json_string = json.dumps(data_sQUOTES) # get string with all double quotes
#print(json_string)

#now we have json


#print(data_sQUOTES['initialProps']['data']['advert']['location']['coordinates'])
#with open('data.txt', 'w') as outfile:



#FIN_json = json.dumps(data_sQUOTES['initialProps']['data']['advert']['location']['coordinates'])

#FIN_json = json.dumps(data_sQUOTES['initialProps']['data']['advert']['location']['coordinates'])
#save_data.append(FIN_json)

#save_data = []
#print(save_data)

#df = pd.read()


#with open('dataNEW.json', 'w') as out:
    #json.dump(FIN_json, out)
    



















