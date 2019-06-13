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


pickle_out = open("city_hrefs","wb")
pickle.dump(url_list,pickle_out)
pickle_out.close()

