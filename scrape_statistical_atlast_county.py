"""

scrape_statistical_atlast_county.py file.
This file contains the script to scrape the county house-hold income data
off of statisticalatlast.com
Author: Samuel Parker.

"""

import gzip
import bs4
import urllib.request
import pandas as pd
import pickle
import os
import time

url_base = 'https://statisticalatlas.com'

# on iteration 7:
start = time.time()

pickle_in = pickle.load(file=open("scrape_assignment_county_7","rb"))


URLZ = []
Allting = {}

for pickled in pickle_in:
    ny_straeng = pickled[:len(pickled)-8]
    ny_straeng = ny_straeng + "Household-Income"
    ny_straeng =  url_base + ny_straeng
    URLZ.append(ny_straeng)


for straeng in URLZ:
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
        time.sleep(0.5)


    except Exception as e:
        print(ny_straeng + " didn't work")
        print(e)


     #Saving it
filnamn = 'skrapad_län_7'
pickle_out = open(filnamn,'wb')
print(type(Allting))
pickle.dump(Allting,pickle_out)
pickle_out.close()

end = time.time()

print("Tidskrav")
print(end-start)

