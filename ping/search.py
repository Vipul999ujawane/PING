from urllib import parse, request

import requests
import xlwt
from bs4 import BeautifulSoup
from pycookiecheat import chrome_cookies

from ping.urls import HOME_URL, PROF_URl
import ping.ping

def get_prof_ids(keyword, url=PROF_URl, num_page = 1, strict = True):
    if(num_page==0):
        return []
    ids = []
    cookies = chrome_cookies(HOME_URL)
    if(url == PROF_URl):
        if(strict==True):
            params = {"view_op": "search_authors", "mauthors": ("label:{0}").format(keyword)}
        else:
            params = {"view_op": "search_authors", "mauthors": ("{0}").format(keyword)}
        r = requests.get(url, params=params, cookies=cookies)
    else:
        r = requests.get(url,cookies=cookies)
    soup = BeautifulSoup(r.content, "html.parser")
    urls = soup.find_all("div", {"class": "gsc_oai"})
    for i in urls:
        parsed = i.find("a")['href']
        id = parse.parse_qs(parse.urlparse(parsed).query)['user'][0]
        ids.append(id)
    try:
        next_page = soup.find("div",{"id":"gsc_authors_bottom_pag"})
        next_link=next_page.find_all("button",{"aria-label":"Next"})[0]
        next_url = next_link['onclick'].split("window.location=")[1]
        next_url = next_url.replace("'","")
        next_url = next_url.encode("utf-8").decode('unicode_escape')
        parent_url2 = HOME_URL + next_url
        ids += get_prof_ids(keyword,url = parent_url2,num_page=num_page-1)
    except (KeyError, AttributeError):
        return ids
    return ids

def get_jaccard_coefficient(list1, list2):
    intersection = len(set(list1).intersection(list2))
    union = len(list1) + len(list2) - intersection
    return float(intersection/union)

def sort_profs(prof_list,keywords):
    for i in prof_list:
        jaccard_similarity = get_jaccard_coefficient(i.tags,keywords)
        print("[*] Prof : {0} | Jaccard Similarity : {1}".format(i.name,jaccard_similarity))        

def create_xls(prof_list):
    wb = xlwt.Workbook()
    ws = wb.add_sheet("Sheet 1")
    ws.write(0, 0, "Name")
    ws.write(0, 1, "Job")
    ws.write(0, 2, "University")
    ws.write(0, 3, "Homepage")
    ws.write(0, 4, "H-Index")
    ws.write(0, 5, "Labels")
    ws.write(0,6,"Google Scholar Link")
    iterator=1
    for i in prof_list:
        ws.write(iterator, 0, i.name)
        ws.write(iterator, 1, i.job)
        ws.write(iterator, 2, i.university)
        if(i.homepage==None):
            ws.write(iterator, 3, "N/A")
        else:    
            ws.write(iterator, 3, xlwt.Formula('HYPERLINK("%s";"HOMEPAGE")'%i.homepage))
        ws.write(iterator, 4, str(i.h_index))
        ws.write(iterator, 5, str(i.tags))
        ws.write(iterator, 6, xlwt.Formula('HYPERLINK("%s";"GOOGLE SCHOLAR")'%i.gs_link))
        iterator += 1
    wb.save("Data.xls")
    print("[*] Data Saved to Data.xls")