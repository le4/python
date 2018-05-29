#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from websocket import create_connection
import time, gzip
import json

if __name__ == '__main__':
    while (1):
        try:
            ws = create_connection("wss://ws-feed.gdax.com/")
            break
        except:
            print('connect ws error,retry...')
            time.sleep(5)

    # 订阅 KLine 数据
    # tradeStr="""{"sub": "market.ethusdt.kline.1min","id": "id10"}"""

    # 请求 KLine 数据
    # tradeStr="""{"req": "market.ethusdt.kline.1min","id": "id10", "from": 1513391453, "to": 1513392453}"""

    # 订阅 Market Depth 数据
    # tradeStr="""{"sub": "market.ethusdt.depth.step5", "id": "id10"}"""

    # 请求 Market Depth 数据
    # tradeStr="""{"req": "market.ethusdt.depth.step5", "id": "id10"}"""

    # 订阅 Trade Detail 数据
    # tradeStr="""{"sub": "market.ethusdt.trade.detail", "id": "id10"}"""

    # 请求 Trade Detail 数据
    # tradeStr = """{"req": "market.htusdt.trade.detail", "id": "id10"}"""

    # 请求 Market Detail 数据
    # tradeStr="""{"req": "market.ethusdt.detail", "id": "id12"}"""

    tradeStr = """{"type":"subscribe","channels":[{"name":"status","product_ids":[]},{"name":"level2_50","product_ids":["BTC-USD"]},{"name":"user","product_ids":["BTC-USD","BTC-EUR","BTC-GBP","ETH-USD","ETH-EUR","ETH-BTC","LTC-USD","LTC-EUR","LTC-BTC","BCH-USD","BCH-EUR","BCH-BTC"]},{"name":"ticker_1000","product_ids":["BCH-BTC","BCH-USD","BTC-EUR","BTC-GBP","BTC-USD","ETH-BTC","ETH-EUR","ETH-USD","LTC-BTC","LTC-EUR","LTC-USD","BCH-EUR"]},{"name":"matches","product_ids":["BTC-USD"]}]}"""

    ws.send(tradeStr)
    while (1):
        compressData = ws.recv()
        if compressData[:15] == '{"type":"match"':
            print("成交:" + compressData)
