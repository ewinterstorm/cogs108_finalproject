"""" scrape_statistical_atlas.py file.
    This file was used to scrape data about houssehold income
     off of statisticalatlas.com
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

exit()
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
