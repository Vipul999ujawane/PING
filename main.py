#!/usr/bin/env python3

from urllib import parse
from ping.ping import Ping
from ping.urls import PROF_URl,HOME_URL
from ping.search import get_prof_ids
from bs4 import BeautifulSoup
import numpy as np
import time
import requests
import xlwt
from pycookiecheat import chrome_cookies


def get_keywords():
    keywords = []
    with open("keywords.txt", "r") as f:
        lines = f.readlines()
        for l in lines:
            keywords.append(l.replace('\n', ''))
    return keywords


if(__name__ == "__main__"):
    print("[*] Ping Started")
    keywords = get_keywords()
    final_id = set()
    print(("[+] {0} Keywords Acquired").format(keywords.__len__()))
    for word in keywords:
        print("[*] Searching for keyword: "+word)
        print("[+] Searching Proffessors")
        ids = get_prof_ids(keyword=word,num_page=2)
        # time.sleep((30-5)*np.random.random()+5)
        # Use this to prevent flagging. Makes code slower but safe to use.
        for id in ids:
            final_id.add(id)
    wb = xlwt.Workbook()
    ws = wb.add_sheet("Sheet 1")
    ws.write(0, 0, "Name")
    ws.write(0, 1, "Job")
    ws.write(0, 2, "University")
    ws.write(0, 3, "Homepage")
    ws.write(0, 4, "H-Index")
    ws.write(0, 5, "Labels")
    ws.write(0,6,"Google Scholar Link")
    iterator = 1
    for id in final_id:
        ping = Ping(id)
        print(("[+] Professor {0}").format(ping.name))
        ws.write(iterator, 0, ping.name)
        ws.write(iterator, 1, ping.job)
        ws.write(iterator, 2, ping.university)
        ws.write(iterator, 3, xlwt.Formula('HYPERLINK("%s";"HOMEPAGE")'%ping.homepage))
        ws.write(iterator, 4, str(ping.h_index))
        ws.write(iterator, 5, str(ping.tags))
        ws.write(iterator, 6, xlwt.Formula('HYPERLINK("%s";"GOOGLE SCHOLAR")'%ping.gs_link))
        iterator += 1
    wb.save("Data.xls")
    print("[*] Data Saved to Data.xls")