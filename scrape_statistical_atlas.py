import gzip
import bs4
import urllib.request
import pandas as pd
import pickle
import os
import time
#url_base22 = 'https://statisticalatlas.com/county/California/San-Francisco-County/Household-Income'
url_base = 'https://statisticalatlas.com'

#counties = ["California/San-Francisco-County","California/Los-Angeles-County","California/San-Diego-County","Utah/Salt-Lake-County","Texas/Dallas-County","Florida/Miami-Dade-County","Michigan/Wayne-County","New-York/Bronx-County"]

#Straengen = "San Francisco, California, Los-Angeles-County, CA , San-Diego-County Salt Lake County, dallas, Miami-Dade,Wayne County, Bronx-County"
#req = urllib.request.Request(url_base4, headers = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'})


## next up is 2
pickle_in = pickle.load(file=open("scrape_assignment2","rb"))



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
        time.sleep(1)




    except Exception as e:
        print(ny_straeng + " didn't work")
        print(e)




     #Saving it
filnamn = 'allting_scraped3'
pickle_out = open(filnamn,'wb')
print(type(Allting))
pickle.dump(Allting,pickle_out)
pickle_out.close()


"""

import os
print(os.path.exists)

#print(contents)



#data_frame = pd.DataFrame(columns=['Percentile','Income','Percentage'])




source = urllib.request.urlopen(req)
soup = bs4.BeautifulSoup(source,features="lxml")
print(source)
print(soup)
"""