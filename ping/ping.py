import re

import requests
from bs4 import BeautifulSoup
from pycookiecheat import chrome_cookies

from ping.urls import HOME_URL, PROF_URl


class Ping:
    id=""
    html=""
    name=""
    university=""
    job = ""
    h_index=""
    homepage=""
    gs_link=""
    tags=[]
    def __init__(self,id):
        self.id = id
        params = {"user":id}
        cookies=chrome_cookies(PROF_URl)
        r = requests.get(PROF_URl,params=params,cookies=cookies)
        self.html = BeautifulSoup(r.content,"html.parser")
        self.name = self.get_name()
        self.university=self.get_university()
        self.job=self.get_job()
        self.h_index = self.get_h_index()
        self.homepage = self.get_homepage()
        self.tags=self.get_tags()
        self.gs_link = r.url

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
