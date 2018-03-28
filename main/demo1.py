#!/usr/bin/python3
# -*- coding: UTF-8 -*-


import urllib.request
import re
import os, time
import urllib
import requests
from bs4 import BeautifulSoup
import sys
import socket

socket.setdefaulttimeout(20)  # 设置socket层的超时时间为20秒

baseurl = "http://96xxnet1.com"
urls = ["http://96xxnet1.com/tuinvlang/1855.html"]
for i in range(2, 5):
    ss = "http://96xxnet1.com/tuinvlang/1855_" + str(i) + ".html"
    urls.append(ss)

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
    'If-None-Match': match
}

path = 'E://meitu/'
targetDir = "E://meitu/"  # 文件保存路径


# 获取html
def getHtml(tempUrl):
    requset = requests.get(tempUrl, headers=headers)
    requset.encoding = "gb2312"
    html = requset.text
    return html


def destFile(path):
    if not os.path.isdir(targetDir):
        os.mkdir(targetDir)
    pos = path.rindex('/')
    t = os.path.join(targetDir, path[pos + 1:])
    return t


if __name__ == '__main__':
    for url in urls:
        rowHtml = getHtml(url)
        rowSoup = BeautifulSoup(rowHtml, 'html.parser')
        for tag in rowSoup.find_all("article"):
            itemlist = tag.find_all("img")
            for img in itemlist:
                time.sleep(4)
                imglink = baseurl + img.attrs['src']
                print(imglink)
                try:
                    urllib.request.urlretrieve(imglink, destFile(imglink))  # 下载图片
                    print("保存成功...")
                    # html = requests.get(imglink, headers=headers)
                    # file_name = imglink.split(r'/')[-1]
                    # f = open(path + file_name, 'wb')
                    # f.write(html.content)
                    # f.close()
                except UnicodeDecodeError as e:
                    print('-----UnicodeDecodeError url:', url)
                except urllib.error.URLError as e:
                    print("-----urlError url:", url)
                except socket.timeout as e:
                    print("-----socket timout:", url)
