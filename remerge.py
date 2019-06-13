""" remerge.py file. This file was used to merge back together chunks of scraped data.
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

dic1 = pickle.load(file=open("skrapad_län_0","rb"))
dic2 = pickle.load(file=open("skrapad_län_1","rb"))
dic3 = pickle.load(file=open("skrapad_län_2","rb"))
dic4 = pickle.load(file=open("skrapad_län_3","rb"))
dic5 = pickle.load(file=open("skrapad_län_4","rb"))
dic6 = pickle.load(file=open("skrapad_län_5","rb"))
dic7 = pickle.load(file=open("skrapad_län_6","rb"))
dic8 = pickle.load(file=open("skrapad_län_7","rb"))

ordboksLista = [dic1,dic2,dic3,dic4,dic5,dic6,dic7,dic8]

for underOrdbok in ordboksLista:
    for nyckel in underOrdbok:
        HuvudOrdBoken[nyckel] = underOrdbok[nyckel]



pickle_out = open("remerged_data_county","wb")
pickle.dump(HuvudOrdBoken,pickle_out)
pickle_out.close()
