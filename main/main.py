#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import urllib.request
import re
import os
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36'
}

targetDir = r"/Users/shenyiya/Desktop/image"  # 文件保存路径
url = "http://www.lofter.com/tag/%E9%A3%8E%E6%99%AF"


def destFile(path):
    if not os.path.isdir(targetDir):
        os.mkdir(targetDir)
    pos = path.rindex('/')
    t = os.path.join(targetDir, path[pos + 1:])
    return t


request = urllib.request.Request(url, headers=header)

reponse = urllib.request.urlopen(request).read()

body = str(reponse, "utf-8")

for link, t in set(re.findall(r'(http:[^\s]*?(jpg|png|gif))', body)):  # 正则表达式查找所有的图片
    print(link)
    try:
        urllib.request.urlretrieve(link, destFile(link))  # 下载图片
    except:
        print('失败')  # 异常抛出
