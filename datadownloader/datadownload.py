#! /usr/bin/env python3
import requests
import os
import shutil
from bs4 import BeautifulSoup as bs
import warnings
import re
from nltk.tokenize.casual import URLS
import time

"""ref: https://www.talaikis.com/15-years-of-forex-tick-data-to-mongodb-using-python-part-one/"""

global dump

def download_file(url_):
    '''download file magic'''
    global dump
    file = requests.get(url_, stream=True)
    dump = file.raw

def save_file(path_, file_name):
    '''file saving magic'''
    global dump
    location = os.path.abspath(path_)
    with open(file_name, 'wb') as location:
        shutil.copyfileobj(dump, location)
    del dump

if __name__ == "__main__":
    scriptStart = time.time()

    # suppress security warnings
    warnings.filterwarnings("ignore")

    # starting point
    src_ = "http://ratedata.gaincapital.com/"

    # initialize session
    s = requests.Session()

    # request www
    r = s.get(src_, verify=False)

    # get html object
    html_ = r.text
    soup = bs(html_)

    # get first level links
    first_level = []
    for link in soup.find_all('a'):
        l = link.get('href')
        if "0" in l:
            first_level.append(src_ + l[2:])

    # get second level
    next_level = []
    to_down = []

    for i in range(len(first_level)):
        print(first_level[i])
        r2 = s.get(first_level[i], verify=False)
        html_2 = r2.text
        soup = bs(html_2)
        for link in soup.find_all('a'):
            l = link.get('href')

            # find new data format strings
            f = re.findall(r'(?<!\d)\d{1,2}\s', l)
            if len(f) > 0:
                next_level.append(first_level[i] + "/" + l[2:])
            # if zip add to final list
            if ".zip" in l:
                to_down.append(first_level[i] + "/" + l[2:])

    #make unique list of next level
    next_level = list(set(next_level))

    # get urls for new data format
    for i in range(len(next_level)):
        print(next_level[i])

        r3 = s.get(next_level[i], verify=False)
        html_3 = r3.text
        soup = bs(html_3)
        for link in soup.find_all('a'):
            l = link.get('href')

            # if this is zip file add to list to download_file
            if ".zip" in l:
                to_down.append(next_level[i] + "/" + l[2:])
    s.close()

    # make list_unique
    to_down = list(set(to_down))

    for g in range(len(to_down)):
        # open Session
        s. requests.Session()
        print("Downloading %s" % to_down[g])

        #make name of file and path
        file_name = to_down[g][31:].replace("/", "").replace(" ", "")
        print(file_name)
        path_ = os.path.join("/Users/PoFA/DATAFILES/FX/CAPITALGAIN",file_name)

        # do magic
        download_file(to_down[g])
        save_file(to_down[g], path_)

        # close Session
        s.close()
    timeused = (time.time() - scriptStart)/60
    print("Done in %f minutes" % timeused)
