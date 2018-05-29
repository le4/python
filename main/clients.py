#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from websocket import create_connection
import time, gzip
import json

if __name__ == '__main__':
    while (1):
        try:
            ws = create_connection("wss://api.huobipro.com/ws")
            break
        except:
            print('connect ws error,retry...')
            time.sleep(5)

    # 订阅 KLine 数据
    # tradeStr="""{"sub": "market.ethusdt.kline.1min","id": "id10"}"""

    # 请求 KLine 数据
    tradeStr="""{"req": "market.btcusdt.kline.60min","id": "id10", "from": 1524124564, "to": 1525204564}"""

    # 订阅 Market Depth 数据
    # tradeStr="""{"sub": "market.ethusdt.depth.step5", "id": "id10"}"""

    # 请求 Market Depth 数据
    # tradeStr="""{"req": "market.ethusdt.depth.step5", "id": "id10"}"""

    # 订阅 Trade Detail 数据
    # tradeStr="""{"sub": "market.ethusdt.trade.detail", "id": "id10"}"""

    # 请求 Trade Detail 数据
    #tradeStr = """{"req": "market.htusdt.trade.detail", "id": "id10"}"""

    # 请求 Market Detail 数据
    # tradeStr="""{"req": "market.ethusdt.detail", "id": "id12"}"""

    ws.send(tradeStr)
    while (1):
        compressData = ws.recv()
        result = gzip.decompress(compressData).decode('utf-8')
        print(result)
        if result[:7] == '{"ping"':
            ts = result[8:21]
            pong = '{"pong":' + ts + '}'
            ws.send(pong)
            ws.send(tradeStr)
        else:
            detail = json.loads(result)
            array = detail['data']
            array.reverse()
            for item in array:
                time_local = time.localtime(item['ts'] / 1000)
                dt = time.strftime("%H:%M:%S", time_local)
                if (item['direction'] == 'buy'):
                    type = "卖出"
                    print("%s  %.4f \033[1;31m %s \033[0m  %s  " % (dt, item['price'], type, item['amount']))
                else:
                    type = "买入"
                    print("%s  %.4f \033[1;32m %s \033[0m  %s  " % (dt, item['price'], type, item['amount']))

