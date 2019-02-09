#!/usr/bin/env python3

from urllib import parse
from ping.ping import Ping
from ping.urls import PROF_URl
from bs4 import BeautifulSoup
import requests
def get_keywords():
    keywords=[]
    with open("keywords.txt","r") as f:
        lines = f.readlines()
        for l in lines:
            keywords.append(l.replace('\n',''))
    return keywords

def get_prof_ids(keyword):
    ids=[]
    params = {"view_op":"search_authors","mauthors":keyword}
    r = requests.get(PROF_URl,params=params)
    soup = BeautifulSoup(r.content,"html.parser")
    urls = soup.find_all("div",{"class":"gsc_oai"})
    for i in urls:
        ids.append(parse.parse_qs(parse.urlparse(i.find("a")['href']).query)['user'][0])
    return ids

if(__name__=="__main__"):
    keywords = get_keywords()
    for word in keywords:
        print(word)
    ids = get_prof_ids(keywords[0])
    for id in ids:
        ping = Ping(id)
        print(ping.name)