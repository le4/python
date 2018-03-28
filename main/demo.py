#!/usr/bin/python3
# -*- coding: UTF-8 -*-


import urllib.request
import re
import os
import urllib
import requests
from bs4 import BeautifulSoup
import sys

baseurl = "http://96xxnet1.com"
url = baseurl + "/tuinvlang/"

match = "52bc715737c3d31:0"
# 添加请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36',
    'Referer': 'http://96xxnet1.com/tuinvlang/',
    'Upgrade-Insecure-Requests': "1",
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cache-Control': 'max-age=0',
    'Host': '96xxnet1.com',
    'Cookie': 'UM_distinctid=1626311e6f1848-04f4ebc0e8512e-3a61430c-100200-1626311e6f2321; CNZZDATA1255630433=1566942871-1522079944-http%253A%252F%252F96xxnet1.com%252F%7C1522162972',
    'Connection': 'keep-alive',
    'If-None-Match': match
}


# 获取html
def getHtml(tempUrl):
    requset = requests.get(tempUrl, headers=headers)
    requset.encoding = "gb2312"
    html = requset.text
    return html

# 过滤首页获得每个首页的item
requset = requests.get(url, headers=headers)
requset.encoding = "gb2312"
html = requset.text
soup = BeautifulSoup(html, 'html.parser')
for tag in soup.find_all('h2'):
    row = tag.contents[0]
    rowHtml = getHtml(baseurl + row.attrs['href'])
    rowSoup = BeautifulSoup(rowHtml, 'html.parser')
    # article=rowSoup.find("article")
    print(rowSoup)
# print(soup)  # 可以看到网页的内容
