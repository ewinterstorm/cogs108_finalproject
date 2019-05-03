import pickle
import pandas as pd
import numpy as np
import os


percentiles = ["95th","80th","60th","Median","40th","20th"]


counties = ["California\\San-Francisco-County","California\\Los-Angeles-County","California/San-Diego-County","Utah/Salt-Lake-County","Texas/Dallas-County","Florida/Miami-Dade-County","Michigan/Wayne-County","New-York/Bronx-County"]
data_ramar = []
for county in counties:
    place = []
    income = []
    percent = []

    print(county)
    filnamn = county+"\\scraped"
    cwd = os.getcwd()
    pickle_in = open(filnamn, 'rb')
    contents = pickle.load(pickle_in)
    pickle_in.close()


    namn_rad = []

    data_ram = pd.DataFrame(columns=['place', 'percentile', 'income', 'percent'])

    for a in contents:
        if "Percentile" in a or "Median" in a:
            #percentiles.append(a)
            pass
        elif "$" in a:
            income.append(pd.Series(a.split('$')[1]))
        elif "%" in a:
            percent.append(pd.Series(a.split("%")[0]))
        namn_rad.append(county)

    print(income)
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


oever_dr = pd.concat(data_ramar)

oever_dr.to_csv("out.csv")

print(oever_dr)



