#!/usr/bin/env python3

import time
from urllib import parse

import numpy as np
import requests
import xlwt
from bs4 import BeautifulSoup
from pycookiecheat import chrome_cookies
import argparse
from ping.ping import Ping
from ping.search import get_prof_ids, sort_profs, create_xls
from ping.urls import HOME_URL, PROF_URl


def get_keywords(filename):
    keywords = []
    with open(filename, "r") as f:
        lines = f.readlines()
        for l in lines:
            keywords.append(l.replace('\n', ''))
    return keywords


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file",help="Input File for Keywords")
    parser.add_argument("output",help="Output File for xls. Must ends with a .xls ")
    parser.add_argument("-s","--strict",action="store_true",help="Use search in the strict mode")
    parser.add_argument("-n","--number",help="Number of Pages for search per keyword. Default = 2",type=int)
    args = parser.parse_args()
    input_file = args.file
    output_file = args.output
    strict = False
    pageNum=2
    if(args.strict):
        strict=True
    if(args.number):
        pageNum=args.number
    try:
        print("[*] Ping Started")
        print("[#] Number of Pages to Search : {0}".format(pageNum))
        print("[#] Strict Mode : {0}".format(strict))
        print("[#] Getting Keywords From : {0}".format(input_file))
        print("[#] Saving Data To : {0}".format(output_file))
        keywords = get_keywords(input_file)
        final_id = set()
        print(("[+] {0} Keywords Acquired").format(keywords.__len__()))
        for word in keywords:
            print("[*] Searching for keyword: "+word)
            print("[+] Searching Professors")
            ids = get_prof_ids(keyword=word,num_page=pageNum, strict=strict)
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
        create_xls(prof_list,output_file)
    except ImportError:
        print("[!] Please Install All Prerequisites")
    except  (Exception,KeyboardInterrupt):
        print("[!] Code Interrupted. Exiting")

if(__name__=="__main__"):
    main()
