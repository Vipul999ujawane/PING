#!/usr/bin/env python3

from urllib import parse
from ping.ping import Ping
from ping.urls import PROF_URl
from bs4 import BeautifulSoup
import numpy as np
import time
import requests
import xlwt
from pycookiecheat import chrome_cookies
def get_keywords():
    keywords=[]
    with open("keywords.txt","r") as f:
        lines = f.readlines()
        for l in lines:
            keywords.append(l.replace('\n',''))
    return keywords

def get_prof_ids(keyword):
    ids=[]
    cookies = chrome_cookies(PROF_URl) #Use Cookies from browser to validate sessions after being flagged off for captcha
    params = {"view_op":"search_authors","mauthors":keyword}
    r = requests.get(PROF_URl,params=params,cookies=cookies)
    soup = BeautifulSoup(r.content,"html.parser")
    urls = soup.find_all("div",{"class":"gsc_oai"})
    for i in urls:
        id =parse.parse_qs(parse.urlparse(i.find("a")['href']).query)['user'][0]
        ids.append(id)
        #print(id)
    return ids

if(__name__=="__main__"):
    keywords = get_keywords()
    final_id = set()
    for word in keywords:
        print(word)
        ids = get_prof_ids(word)
        time.sleep((30-5)*np.random.random()+5) #Use this to prevent flagging. Makes code slower but safe to use.
        for id in ids:
            final_id.add(id)
    for id in final_id:
        ping = Ping(id)
        print(ping.name)