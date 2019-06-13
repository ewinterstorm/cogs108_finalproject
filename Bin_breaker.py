"""
Bin_breaker.py file. This was used to break up a list of stuff (like h-refs)
and break it up into a certain number of chunks. This easened the task of
scraping by not needing to do it all at once.
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



Break_bin(pickle_in,8,"scrape_assignment_county_")