#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 14 15:36:11 2019

@author: danielobennett
"""


#import numpy as np
import pandas as pd

#webscraping
#import requests
from bs4 import BeautifulSoup
import pickle
import time

from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
import os


chromedriver = "/usr/local/bin/chromedriver" # path to the chromedriver exe
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)

#check the below text in the html doc mean you have been blocked
robo_txt = "Access to this page has been denied because we believe you are using automation"
def GetMetrics(URL): #, input_df > return df_update  #maybe add df to add to??
    '''
    Processes all of the data that we need to extract from each listing webspage.
    pauses for human Captcha input if it finds it on the webapage
    NOTE: This script requires "Babysitting" ie:
    you may be locked out of the website and be forced to solve the CAPTCHA to continue
    
    '''
    data_d = {} #dict to collect data from each page
    try:
        driver.get(URL)
        time.sleep(8)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        html_doc = str(soup)
        if robo_txt in html_doc:
            print("Please solve the Captcha")
            time.sleep(15)
            print("hope you solved it! Heres more time.. just incase")
            time.sleep(25)
            print("last bit...")
            time.sleep(15)
            #repeat to re-grab the webpage??
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            html_doc = str(soup)

        #Finds the title of the posting > try to split up rn???
        title_index = html_doc.find('<title>')
        title = html_doc[title_index+6:title_index+100]
    
        #finds the rent for each listing
        rent_index = html_doc.find('<span class="h3 typeEmphasize">')
        rent = html_doc[rent_index+31:rent_index+80].strip()
        
        #bedroom stuff    >>>> /NEW
        bed_index = html_doc.find('class="iconBed">')
        bed       = html_doc[bed_index+8:bed_index+90].split('>')[1].split('<')[0].strip()

        #bathroom stuff  >>>? NEW
        bath_index = html_doc.find('class="iconBath">')
        bath       = html_doc[bath_index+8:bath_index+90].split('>')[1].split('<')[0].strip()    
    
        #finds the number of days on trullia
        days_index = html_doc.find('days on Trulia')
        days = html_doc[days_index-4:days_index+1].strip().split(" ")[0]
    
        #finds the neighborhood
        barrio_index = html_doc.find('<a class="linkLowlight linkUnderline" href=')
        barrio = html_doc[barrio_index+40:barrio_index+120].split('>')[1].split('<')[0]

        #finds the elevation
        elev_index = html_doc.find('<td>Elevation of property</td>')
        elev = html_doc[elev_index+30:elev_index+50].split('>')[1].split('<')[0]
    
        #Finds the number of trees near apartment
        tree_index = html_doc.find('<td>Tree Cover of lot</td>')
        tree = html_doc[tree_index+30:tree_index+50].split('>')[1].split('<')[0]
    
        #Distance to Starbucks
        starb_index = html_doc.find('<td>Starbucks Distance</td>')
        starb = html_doc[starb_index+30:starb_index+50].split('>')[1].split('<')[0]
    
        ##Sq ftage of aprtment (not always constant)
        sqft_index = html_doc.find('"iconFloorplan')
        sqft = html_doc[sqft_index+9:sqft_index+90].split('>')[1].split('<')[0]
    
        #Pets or not. if "No pets allowed" not in check after 
        pet_index = html_doc.find('<li class="iconDog">')
        pet = html_doc[pet_index+19:pet_index+70].split('>')[1].split('<')[0].strip()
        
        #get string of amenities listed
        amen_strt_index = html_doc.find('<ul class="mbn">')
        amen_end_index = html_doc.find('Certain features are not guaranteed')
        amenities = html_doc[amen_strt_index+17:amen_end_index-55]
        
        #get number of landmarks nearby
        landmrk_start_index = html_doc.find('<td>Landmarks</td>')
        landmrk_end_index   = html_doc.find('<table class="table tableBasic mtl">')
        lm_temp             = html_doc[landmrk_start_index:landmrk_end_index]
        landmarks           = lm_temp.count(',')
        if landmarks == 0:
            landmarks == 1 # assume no commas mean that there is one landmark 
            
        #assigning to dictionary
        data_d['Title'] = title
        data_d['Rent'] = rent
        data_d['Days_Posted'] = days
        data_d["Neighborhood"] = barrio
        data_d["Elevation"] = elev
        data_d["Tree_Cover_Pct"] = tree
        data_d["Starbucks_dist"] = starb
        data_d["Sqft"] = sqft
        data_d["Pets Allowed?"] = pet 
        data_d["Link"] =  URL 
        data_d["Amenties"] = amenities  #requires additional cleaning..
        data_d["Landmarks"] = landmarks
        data_d["Bedrooms"]  = bed
        data_d["Bathroom"]  = bath       

        return data_d
    except:
        return data_d


#to remove afterwards
with open('new_list.pkl', 'rb') as picklefile: 
    list_links = pickle.load(picklefile)

unit_test = list_links[1:201]  #do in small batches for ease

counter = 0 #keep track of links
final_df = pd.DataFrame() #empty dataframe to collect results
user_agent = {'User-agent': 'Mozilla/5.0'} # for requests

for link in unit_test:
    time.sleep(3)
    counter += 1
    temp_dict = GetMetrics(link)
    temp_df = pd.DataFrame(temp_dict, index=[0])
    final_df = pd.concat([final_df,temp_df], axis=0) #Append temp dataframe to final data frame
    print("Link # : " , str(counter), "length of dict " , str(len(temp_dict)) + "size of final df" + str(final_df.shape))
    if counter % 10 == 0:
        with open('final_df.pkl', 'wb') as picklefile:
            pickle.dump(final_df, picklefile)
with open('final_df.pkl', 'wb') as picklefile:
    pickle.dump(final_df, picklefile)
print("finished processing!!!")
print(final_df.shape)
driver.close()

