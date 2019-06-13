"""
This script gets the URL to the page of every major city in the US. It searches by state.
Once it collects all of those URLS, then those URLS can be fed into the scrape_statistical_atlast.py file
so that we can scrape up the data for every city.
Author: Samuel Parker
"""


import gzip
import bs4
import urllib.request
import pandas as pd
import pickle
import os
import re

states = ["Alabama","Alaska","Arizona","Arkansas","California","Colorado","Connecticut","Delaware","Florida","Georgia",
          "Hawaii","Idaho","Illinois","Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland",
          "Massachusetts","Michigan", "Minnesota","Mississippi","Missouri","Montana","Nebraska","Nevada","New-Hampshire","New-Jersey",
          "New-Mexico","New-York","North-Carolina","North-Dakota","Ohio","Oklahoma","Oregon","Pennsylvania",
          "Rhode-Island","South-Carolina","Tennessee","Texas","Utah","Vermont","Virginia","Washington","West-Virginia",
          "Wisconsin","Wyoming"]

url_base = 'https://statisticalatlas.com/state/'

url_list = []


for state in states:
    try:
        target_url = url_base + state + "/Overview"
        request = urllib.request.Request(
            target_url,
            headers={
                "Accept-Encoding": "gzip",
                "User-Agent": "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11",
            })
        response = urllib.request.urlopen(request)
        gzip_dec = gzip.decompress(response.read())
        print(gzip_dec)
        gzipFile = gzip.GzipFile(fileobj=response)
        gzipFile.read()

        soup = bs4.BeautifulSoup(gzip_dec,features="lxml")

        vaart_steg = soup.find_all('div', class_="info-table-contents-td col-sm-9")
        vaart_steg = vaart_steg[3]
        vaart_steg = vaart_steg.find_all('a')
        hrefs = []
        for link in vaart_steg:
            if link != None:
                hrefs.append(link['href'])

        url_list += hrefs

    except:
        print("This state didn't work :( %s" %state)

# The URL for each list was put onto a big list.
# this list was serialized / pickled out and handled by another script (I have included it below)

pickle_out = open("city_hrefs","wb")
pickle.dump(url_list,pickle_out)
pickle_out.close()


"""
Bin_breaker.py file. This was used to break up a list of stuff (like h-refs)
and break it up into a certain number of chunks. This easened the task of
scraping by not needing to do it all at once.

This script would be run once

Author: Samuel Parker.
"""

import pickle

pickle_in = pickle.load(file=open("county_hrefs","rb"))

def Break_bin (breakable, bin_count, filnamn):
    storage = {}

    for number in range(bin_count):
        storage[number] = []

    count = 0
    overLength = len(breakable)
    for number in range(len(breakable)):
        storage[count].append(breakable[number])
        count += 1
        if count % bin_count == 0:
            count = 0

    totala_laengden = 0
    count = 0
    for key in storage:
        stycket = storage[key]
        totala_laengden += len(stycket)
        pickle_out = open( (filnamn+str(count)), 'wb')
        pickle.dump(stycket, pickle_out)
        pickle_out.close()
        count += 1

    assert totala_laengden == overLength



Break_bin(pickle_in,8,"scrape_assignment")


""""
    scrape_statistical_atlas.py file.
    This file was used to scrape data about houssehold income
     off of statisticalatlas.com

     This script would be run once for each scraping assignment
     that I created using the binbreaker earlier. In our case,
     we had it run 8 times.

     Author: Samuel Parker
     Approximate date of use: Spring 2019
"""


# Importing libraries.

import gzip
import bs4
import urllib.request
import pandas as pd
import pickle
import os
import time

url_base = 'https://statisticalatlas.com'


## I had broken up the scraping assignments up in the binbreaker. That we don't have to
## scrape literally all of the data at once.
pickle_in = pickle.load(file=open("scrape_assignment7","rb"))

for k in pickle_in:
    print(k)

URLZ = []
Allting = {}

for pickled in pickle_in:
    ny_straeng = pickled[:len(pickled)-8]
    ny_straeng = ny_straeng + "Household-Income"
    ny_straeng =  url_base + ny_straeng
    URLZ.append(ny_straeng)


for straeng in URLZ:
    ## Using a try-catch block, so one exception doesn't jeopardize the whole operation.
    try:
        print(straeng)
        request = urllib.request.Request(
            straeng,
            headers={
                "Accept-Encoding": "gzip",
                "User-Agent": "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11",
            })
        response = urllib.request.urlopen(request)
        gzip_dec = gzip.decompress(response.read())
        print(gzip_dec)
        gzipFile = gzip.GzipFile(fileobj=response)
        gzipFile.read()

        soup = bs4.BeautifulSoup(gzip_dec,features="lxml")

        vaart_steg = soup.body
        vaart_steg = vaart_steg.find("div",class_="figure-container",id="figure/household-income-percentiles")
        vaart_steg = vaart_steg.find("div", class_="figure-contents")
        vaart_steg = vaart_steg.find("svg")

        contents = vaart_steg.find_all("g")
        contents = [a.text for a in contents]

        Allting[straeng] = contents
        print(type(Allting))
        time.sleep(1)



    ## Handling exceptions
    except Exception as e:
        print(ny_straeng + " didn't work")
        print(e)

     #Saving it
filnamn = 'allting_scraped8'
pickle_out = open(filnamn,'wb')
print(type(Allting))
pickle.dump(Allting,pickle_out)
pickle_out.close()




"""
    remerge.py file. This file was used to merge back together chunks of scraped data.
    During the scraping process, I decided to scrape one eighth of all of the cities or
    counties at a time, and in this file, that sraped data gets put back together.
    Author: Samuel Parker
"""

import pandas
import pickle
pickle_in = pickle.load(file=open("city_hrefs","rb"))

url_base = 'https://statisticalatlas.com'

URLZ = []


for pickled in pickle_in:
    ny_straeng = pickled[:len(pickled)-8]
    ny_straeng = ny_straeng + "Household-Income"
    ny_straeng =  url_base + ny_straeng
    URLZ.append(ny_straeng)


HuvudOrdBoken = {}

dic1 = pickle.load(file=open("allting_scraped1","rb"))
dic2 = pickle.load(file=open("allting_scraped2","rb"))
dic3 = pickle.load(file=open("allting_scraped3","rb"))
dic4 = pickle.load(file=open("allting_scraped4","rb"))
dic5 = pickle.load(file=open("allting_scraped5","rb"))
dic6 = pickle.load(file=open("allting_scraped6","rb"))
dic7 = pickle.load(file=open("allting_scraped7","rb"))
dic8 = pickle.load(file=open("allting_scraped8","rb"))

# swedish for  word-books list , e.g. dictionary list
ordboksLista = [dic1,dic2,dic3,dic4,dic5,dic6,dic7,dic8]

for underOrdbok in ordboksLista:
    for nyckel in underOrdbok:
        HuvudOrdBoken[nyckel] = underOrdbok[nyckel]


# At this point, we have a dictionary full of entries that contain all of our data.
pickle_out = open("remerged_data_county","wb")
pickle.dump(HuvudOrdBoken,pickle_out)
pickle_out.close()

"""

This file takes in the data that has been freshly scraped, and spits it out into a CSV.
The CSV would still be in need of more preprocessing, however. But this is a first step.

"""

import pickle
import pandas as pd
import numpy as np
import os

percentiles = ["95th","80th","60th","Median","40th","20th"]
pickle_in = pickle.load(file=open("remerged_data_county","rb"))
data_ramar = []
for nyckel in pickle_in:
    try:
        place = []
        income = []
        percent = []

        namn_rad = []

        contents = pickle_in[nyckel]

        data_ram = pd.DataFrame(columns=['place', 'percentile', 'income', 'percent'])

        for a in contents:
            if "Percentile" in a or "Median" in a:
                #percentiles.append(a)
                pass
            elif "$" in a:
                income.append(pd.Series(a.split('$')[1]))
            elif "%" in a:
                percent.append(pd.Series(a.split("%")[0]))
            namn_rad.append(nyckel)

        #print(income)
        income = income[1:]
        namn_rad = namn_rad[:6]

        #print(len(income),len(namn_rad),len(percentiles))

        income = pd.Series(income)
        percent = pd.Series(percent)
        percentile = pd.Series(percentiles)
        namn_rad = pd.Series(namn_rad)



        data_ram.income = income
        data_ram.percent = percent
        data_ram.percentile = percentiles
        data_ram.place = namn_rad

        data_ramar.append(data_ram)
        #print(data_ram)
    except:
        print("This gave us trouble: ")
        print(nyckel)



oever_dr = pd.concat(data_ramar)

oever_dr.to_csv("income_county.csv")

print(oever_dr)