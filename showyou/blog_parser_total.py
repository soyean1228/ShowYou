import csv
import requests
import time
from bs4 import BeautifulSoup
import urllib.request as req
from itertools import count
from collections import OrderedDict
import re
import datetime
import requests
from bs4 import BeautifulSoup
import csv

#몽고디비
import pymongo
from . import mongo_connection


url='http://search.naver.com/search.naver'
hrd = {'Usere-Agent':'Mozilla/5.0','referer':'http://naver.com'}

def parsing(keyword,day):

    if day == 'm':
        num = 30
    elif day == 'd':
        num = 0
    elif day == 'w':
        num = 7

    end = datetime.date.today()
    start = end - datetime.timedelta(days=num)

    end = end.strftime("%Y%m%d")
    start = start.strftime("%Y%m%d")

    search_date_from = int(end)
    search_date_to = int(start)
    search_date_option = search_date_to - search_date_from -1

    param = {
        'where' : 'post',
        'query' : keyword,
        'date_from' : search_date_from,
        'date_to' : search_date_to,
        'date_option' : search_date_option
    }

    response = requests.get(url,params = param,headers=hrd)
    
    blog_post_list = []
    global i
    i = 0

    def blog_crawling(page):
        global i 
        print(page)
        soup = BeautifulSoup(response.text, 'html.parser')

        blog_post = []

        for links in soup.select('li.sh_blog_top > dl'): 
            
            author = links.select('dd.txt_block a')
            content = links.select('dd.sh_blog_passage')

            author = author[0].text
            content = content[0].text

            blog_info = {}
            blog_info['post_id'] = i
            blog_info['person_id'] = author
            blog_info['post'] = content

            blog_post += [blog_info] 
            i = i+1
        return blog_post

    for index in range(1,10,1):
        blog_post_list += blog_crawling(page = index)

    mongo_connection.post_insert(blog_post_list)
