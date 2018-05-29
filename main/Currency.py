# !/usr/bin/python3
# -*- coding: UTF-8 -*-

import requests
import json
from bs4 import BeautifulSoup
import xlrd
import xlwt

requests.adapters.DEFAULT_RETRIES = 5

Hostreferer = {
    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
    'Referer': 'http://www.mzitu.com',
    'Content-Type': 'application/x-www-form-urlencoded'
}

prourl = "https://l10n-api.huobi.cn/v1/settings/currencys?language=zh"
hadaxurl = "https://api.hadax.com/v1/hadax/settings/currencys?language=zh"
# B网
bittrex = "https://bittrex.com/api/v1.1/public/getmarkets"
# GateIO
gateio = "https://data.gateio.io/api2/1/pairs"


def getProData():
    start_html = requests.get(hadaxurl, headers=Hostreferer)
    print(start_html)
    bean = json.loads(start_html.text)
    arr = bean['data']
    print(arr)
    for i in arr:
        print(i['display-name'])


def getBittrexData():
    start_html = requests.get(bittrex, headers=Hostreferer)
    bean = json.loads(start_html.text)
    arr = bean['result']
    for i in arr:
        if (i['BaseCurrency'] == "ETH"):
            print(i['MarketCurrency'])


def getGateIO():
    start_html = requests.get(gateio, headers=Hostreferer)
    arr = json.loads(start_html.text)
    for i in arr:
        if (i.endswith("_ETH")):
            print(i[0:i.find("_")])


def getCurrencyInfo(currency):
    api = "https://m.feixiaohao.com/currencies/" + currency + "/"
    start_html = requests.get(api, headers=Hostreferer)
    rowSoup = BeautifulSoup(start_html.text, 'html.parser')
    # 币种描述
    desc = rowSoup.find_all(class_="textBox maxHeight")
    if (desc.__len__() > 0):
        print(desc[0].contents[0])
        # 流通市值
        val = rowSoup.find_all(class_="box mainInfo")
        for i in val[1].contents[0].children:
            if (i['class'][0] == "val"):
                ltsz = i.contents[0]
                print(ltsz)
        val1 = rowSoup.find_all(class_="box mainInfo mainInfo2")
        count = 0
        for i in val1[0].contents[0].children:
            if (count == 1):
                print(i.contents[0])
            if (count == 3):
                print(i.contents[0])
            count = count + 1
        # print(rowSoup.prettify())


def readExcel():
    data = xlrd.open_workbook('/Users/shenyiya/Desktop/currency.xlsx')
    table = data.sheets()[0]
    count = 0
    for i in table.col_values(4):
        if (count > 0):
            print(i)
            getCurrencyInfo(i)
        count = count + 1


readExcel()
