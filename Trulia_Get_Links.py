#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 10:27:46 2019

@author: danielobennett
"""

'''
!!!Ultimate Trulia Web-scraping Script!!!
'''

import numpy as np
import pandas as pd

#webscraping
import requests
from bs4 import BeautifulSoup
import pickle
import time


def GetAptListings(URL, list_links):
    '''
    Gets all of the Trullia listings on the home page.
    Takes input URL and the real_list
    Returns: Reallist with new links appended
    '''
    
    user_agent = {'User-agent': 'Mozilla/5.0'}
    try:
        #c = 0   #incase of issues
        r = requests.get(URL, headers = user_agent)
        html_docn = r.text
        soup = BeautifulSoup(html_docn, features="lxml") 
        list_it = [] #list for all website links on 1 page
        for link in soup.findAll('a'):
            list_it.append(link.get('href'))
        for link2 in list_it:
            if "/ny/brooklyn/" in str(link2):
                temp =  "https://www.trulia.com"  + link2
                list_links.append(temp)
        return list_links
    except:
        return list_links

'''
####PART 2:  real script shit to use  
###Getting listing links list of links from the mainpage >> need tp add num_p to the link and good
'''

real_links = [] 
first_url = "https://www.trulia.com/for_rent/Brooklyn,NY/APARTMENT,APARTMENT_COMMUNITY,APARTMENT%7CCONDO%7CTOWNHOUSE,CONDO,COOP,LOFT,TIC_type/"
GetAptListings(first_url, real_links)


for page in range(2,200): #full scrape > for page in range(2,226)
    time.sleep(5)
    print("Processing page:", page, "#ofLinks ", len(real_links))
    new_url = ("https://www.trulia.com/for_rent/Brooklyn,NY/APARTMENT,APARTMENT_COMMUNITY,APARTMENT%7CCONDO%7CTOWNHOUSE,CONDO,COOP,LOFT,TIC_type/"+str(page)+"_p")
    print("link page", new_url[-4:])
    GetAptListings(new_url, real_links)    
    if page % 5 == 0: # save every 5 pages
        with open('new_list.pkl', 'wb') as picklefile:
            pickle.dump(real_links, picklefile)

print(len(real_links))
final_list = list(dict.fromkeys(real_links)) #removes duplicates
print(len(final_list))

print(len(real_links))
with open('new_list.pkl', 'wb') as picklefile:
    pickle.dump(final_list, picklefile)

print("Finished!!!")

