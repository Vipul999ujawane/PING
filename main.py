#!/usr/bin/env python3

from urllib import parse
from ping.ping import Ping
from ping.urls import PROF_URl,HOME_URL
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


def get_prof_ids(keyword):
    ids = []
    cookies = chrome_cookies(PROF_URl)
    # Use Cookies from browser to validate sessions
    # after being flagged off for captcha
    params = {"view_op": "search_authors", "mauthors": keyword}
    parent_url = PROF_URl
    r = requests.get(parent_url, params=params, cookies=cookies)
    soup = BeautifulSoup(r.content, "html.parser")
    urls = soup.find_all("div", {"class": "gsc_oai"})
    for i in urls:
        parsed = i.find("a")['href']
        id = parse.parse_qs(parse.urlparse(parsed).query)['user'][0]
        ids.append(id)
        print(id)
    next_page = soup.find_all("div",{"id":"gsc_authors_bottom_pag"})
    for link in  next_page:
        next=link.find_all("button",{"aria-label":"Next"}) 
    parent_url = HOME_URL + next[0]['onclick'].split("window.location='")[1][:-1]
    r = requests.get(parent_url,cookies=cookies)
    print(r.content)
    return ids


if(__name__ == "__main__"):
    keywords = get_keywords()
    final_id = set()
    for word in keywords:
        print(word)
        ids = get_prof_ids(word)
        # time.sleep((30-5)*np.random.random()+5)
        # Use this to prevent flagging. Makes code slower but safe to use.
    #     for id in ids:
    #         final_id.add(id)
    # wb = xlwt.Workbook()
    # ws = wb.add_sheet("Sheet 1")
    # ws.write(0, 0, "Name")
    # ws.write(0, 1, "Job")
    # ws.write(0, 2, "University")
    # ws.write(0, 3, "Homepage")
    # ws.write(0, 4, "H-Index")
    # ws.write(0, 5, "Labels")
    # ws.write(0,6,"Google Scholar Link")
    # iterator = 1
    # for id in final_id:
    #     ping = Ping(id)
    #     print(ping.name)
    #     ws.write(iterator, 0, ping.name)
    #     ws.write(iterator, 1, ping.job)
    #     ws.write(iterator, 2, ping.university)
    #     ws.write(iterator, 3, xlwt.Formula('HYPERLINK("%s";"HOMEPAGE")'%ping.homepage))
    #     ws.write(iterator, 4, str(ping.h_index))
    #     ws.write(iterator, 5, str(ping.tags))
    #     ws.write(iterator, 6, xlwt.Formula('HYPERLINK("%s";"GOOGLE SCHOLAR")'%ping.gs_link))
    #     iterator += 1
    # wb.save("Data.xls")
