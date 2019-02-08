#!/usr/bin/env python3

from urllib import parse
from ping.ping import Ping
from ping.urls import PROF_URl

def get_keywords():
    keywords=[]
    with open("keywords.txt","r") as f:
        lines = f.readlines()
        for l in lines:
            keywords.append(l.replace('\n','').replace(' ','_'))
    return keywords

if(__name__=="__main__"):
    keywords = get_keywords()
    for word in keywords:
        print(word)