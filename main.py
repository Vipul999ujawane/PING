#!/usr/bin/env python3

import time
from urllib import parse

import numpy as np
import requests
import xlwt
from bs4 import BeautifulSoup
from pycookiecheat import chrome_cookies

from ping.ping import Ping
from ping.search import get_prof_ids, sort_profs, create_xls
from ping.urls import HOME_URL, PROF_URl


def get_keywords():
    keywords = []
    with open("keywords.txt", "r") as f:
        lines = f.readlines()
        for l in lines:
            keywords.append(l.replace('\n', ''))
    return keywords


def main():
    try:
        print("[*] Ping Started")
        keywords = get_keywords()
        final_id = set()
        print(("[+] {0} Keywords Acquired").format(keywords.__len__()))
        for word in keywords:
            print("[*] Searching for keyword: "+word)
            print("[+] Searching Professors")
            ids = get_prof_ids(keyword=word,num_page=2, strict=True)
            print(("[+] Found {0} Professor for Keyword {1}").format(ids.__len__(),word))
            # time.sleep((30-5)*np.random.random()+5)
            # Use this to prevent flagging. Makes code slower but safe to use.
            for id in ids:
                final_id.add(id)
        print(("[*] Found {} Professors for all keywords").format(final_id.__len__()))
        prof_list=[]
        for id in final_id:
            ping = Ping(id)
            print(("[+] Collecting Data for Professor {0}").format(ping.name))
            prof_list.append(ping)     
        sort_profs(prof_list = prof_list,keywords = keywords)
        create_xls(prof_list)
    except ImportError:
        print("[!] Please Install All Prerequisites")
    except  (Exception,KeyboardInterrupt):
        print("[!] Error Occured. Code Exiting : {0}".format (type(Exception).__name__))

if(__name__=="__main__"):
    main()
