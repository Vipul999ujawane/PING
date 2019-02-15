from ping.urls import PROF_URl,HOME_URL
from pycookiecheat import chrome_cookies
import requests
from bs4 import BeautifulSoup
from urllib import parse,request

def get_prof_ids(keyword, url=PROF_URl, num_page = 1):
    if(num_page==0):
        return []
    ids = []
    cookies = chrome_cookies(HOME_URL)
    if(url == PROF_URl):
        params = {"view_op": "search_authors", "mauthors": keyword}
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