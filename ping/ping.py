import requests
from bs4 import BeautifulSoup
from urls import PROF_URl,HOME_URL
import re

class Ping:
    id=""
    html=""
    name=""
    university=""
    job = ""
    h_index=""
    homepage=""
    tags=[]
    def __init__(self,id):
        self.id = id
        params = {"user":id}
        r = requests.get(PROF_URl,params=params)
        self.html = BeautifulSoup(r.content,"html.parser")
        self.name = self.get_name()
        self.university=self.get_university()
        self.job=self.get_job()
        self.h_index = self.get_h_index()
        self.homepage = self.get_homepage()
        self.tags=self.get_tags()

    def get_name(self):
        page = self.html
        try:
            name = page.find("div",id="gsc_prf_in").text
        except AttributeError:
            name = None
        return name 

    def get_university(self):
        page = self.html
        try:
            university = page.find("a",{"class":"gsc_prf_ila"}).text
        except AttributeError:
            university = None
        return university

    def get_job(self):
        page = self.html
        try:
            job = page.find("div",{"class":"gsc_prf_il"}).text
        except AttributeError:
            job = None
        return job

    def get_h_index(self):
        page = self.html
        try:
            h_indices = page.find("td",text="h-index")
            h_index,h_index_5 = h_indices.find_next_sibling("td").text,h_indices.find_next_sibling("td").find_next_sibling("td").text
        except AttributeError:
            h_index=None
            h_index_5=None
        return (h_index,h_index_5)

    def get_homepage(self):
        page = self.html
        try:
            homepage = page.find("a",rel="nofollow")['href']
        except (AttributeError,TypeError):
            homepage=None
        return homepage
    
    def get_tags(self):
        page = self.html
        tags=[]
        try:
            tags_tag=page.find_all("a",{"class":"gsc_prf_inta gs_ibl"})
            for tag in tags_tag:
                tags.append(tag.text)
        except:
            tags = []
        return tags
    
    def get_recent_paper(self):
        params = {"user":self.id,"sortby":"pubdate"}
        r = requests.get(PROF_URl,params=params)
        soup = BeautifulSoup(r.content, "html.parser")
        try:
            paper =soup.find("a",{"class":"gsc_a_at"})
            title =paper.text
            link = paper["data-href"]
            r2 = requests.get(HOME_URL+link)
            soup2 = BeautifulSoup(r2.content,"html.parser")
            try:
                link = soup2.find("a")['href']
                print(link)
            except AttributeError:
                link = link
        except AttributeError:
            title=None
            link=None
        return (title,link)

    def get_most_cited(self):
        params = {"user":self.id}
        r = requests.get(PROF_URl,params=params)
        soup = BeautifulSoup(r.content, "html.parser")
        try:
            paper =soup.find("a",{"class":"gsc_a_at"})
            title =paper.text
            link = paper["data-href"]
            r2 = requests.get(HOME_URL+link)
            soup2 = BeautifulSoup(r2.content,"html.parser")
            try:
                link = soup2.find("a")['href']
                print(link)
            except AttributeError:
                link = link
        except AttributeError:
            title=None
            link=None
        return (title,link)

if(__name__ == "__main__"):
    ping1 = Ping("xDL-rrsAAAAJ")
    print(ping1.name)
    print(ping1.university)
    print(ping1.job)
    print(ping1.h_index)
    print(ping1.homepage)
    print(ping1.tags)
    print(ping1.get_recent_paper())
    print(ping1.get_most_cited())
    print("----------------------")
    ping2 = Ping("k3BxbM4AAAAJ")
    print(ping2.name)
    print(ping2.university)
    print(ping2.job)
    print(ping2.h_index)
    print(ping2.homepage)
    print(ping2.tags)
    print(ping2.get_recent_paper())
    print(ping2.get_most_cited())
    print("----------------------")
    ping3 = Ping("mbaG-mQAAAAJ")
    print(ping3.name)
    print(ping3.university)
    print(ping3.job)
    print(ping3.h_index)
    print(ping3.homepage)
    print(ping3.tags)
    print(ping3.get_recent_paper())
    print(ping3.get_most_cited())