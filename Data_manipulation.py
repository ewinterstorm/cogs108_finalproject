"""

This file takes in the data that has been freshly scraped, and spits it out into a CSV.
The CSV would still be in need of more preprocessing, however.

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



