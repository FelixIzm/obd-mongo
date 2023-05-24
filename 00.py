#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests, re, json
import asyncio,urllib.parse
import csv,sys
import argparse
from bs4 import BeautifulSoup
import pymongo
from pymongo import MongoClient
import multiprocessing
import time

import mymodule


with open('dictionary.json') as f:
    data = f.read()
js = json.loads(data)

myclient = pymongo.MongoClient(js['connect'])
print(js['ip'],js['port'],js['db_name'])
mydb = myclient[js['db_name']]
_set = mydb['settings']

sys.tracebacklimit = None
cookies = {}
headers={}
secret_cookie = "3fbe47cd30daea60fc16041479413da2"
secret_cookie_value = ''
JSESSIONID_value = ''
countPages = ''
headers['User-Agent']='Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0'



#mymodule.hello()
#print(mymodule.fib(10))
mymodule.main()