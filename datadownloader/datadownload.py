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
    src_ = "http:/ratedata.gaincapital.com/"

    # initialize session
    s = requests.Session()

    # request www
    r = s.get(src_, verify=False)

    # get html object
    html_ = r.text
    sour = bs(html_)
