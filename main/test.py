#! /usr/bin/env python
# -*- coding: utf-8 -*-

import time
import DBUtils
import DateUtils
import xlwt
import csv
import codecs

# 创建游标
conn = DBUtils.getSBIConnection()
cursor = conn.cursor()
# 当天的开始时间
startDate = DateUtils.get_current_day()
# 当天的结束时间
endDate = DateUtils.get_tomorrow()
# 昨天的时间
yesterday = DateUtils.get_yesterday()
# 生成excel的时间
today = time.strftime('%Y%m%d', time.localtime(time.time()))


def get_order_match_result_data():
    sql = '''SELECT * FROM t_order_match_result where f_filled_amount>0 and f_price>0 and ceil(f_created_at / 1000)
      BETWEEN unix_timestamp(%s) AND unix_timestamp(%s)'''
    cursor.execute(sql, (startDate, endDate))
    results = cursor.fetchall()
    return results


def write_data_to_excel():
    # 获取返回的数据
    result = get_order_match_result_data()
    # 实例化一个Workbook()对象(即excel文件)
    wbk = xlwt.Workbook()
    # 新建一个名为Sheet1的excel sheet。此处的cell_overwrite_ok =True是为了能对同一个单元格重复操作。
    sheet = wbk.add_sheet(u'交易日记账', cell_overwrite_ok=True)
    write_title_to_execle(sheet)
    r = 1
    # 遍历result中的每个元素。s
    for r in xrange(1, len(result)):
        # 对result的每个子元素作遍历
        row = result[r]
        f_symbol = row['f_symbol']
        currency = f_symbol[:-3]  # 币种
        f_type = row['f_type']
        if (f_type == 2) or (f_type == 4):
            f_type = u'卖出'
        if (f_type == 1) or (f_type == 3):
            f_type = u'买入'
        sheet.write(r, 0, DateUtils.get_yesterday_format())
        sheet.write(r, 1, u'自己')
        sheet.write(r, 2, row['f_user_id'])
        sheet.write(r, 3, u'山田太郎')
        sheet.write(r, 4, currency.upper())
        sheet.write(r, 5, f_type)
        sheet.write(r, 6, row['f_filled_amount'])
        sheet.write(r, 7, row['f_price'])
        sheet.write(r, 8, row['f_price'] * row['f_filled_amount'])
        sheet.write(r, 9, '')
        sheet.write(r, 10,'')
    wbk.save(u'交易日记账_' + today + '.csv')


def write_title_to_execle(sheet):
    # 写入表头s
    sheet.write(0, 0, u"約定日")
    sheet.write(0, 1, u"自己或代理")
    sheet.write(0, 2, u"用户id")
    sheet.write(0, 3, u"用户名称")
    sheet.write(0, 4, u'币种名称')
    sheet.write(0, 5, u'交易类型')
    sheet.write(0, 6, u'成交数量')
    sheet.write(0, 7, u'成交单价')
    sheet.write(0, 8, u'成交金额')
    sheet.write(0, 9, u'对方名字')
    sheet.write(0, 10, u'交易手续费')


def write_date_to_csv():
    with open('交易日记账_' + today + '.csv', 'wb') as csvfile:
        csvfile.write(codecs.BOM_UTF8)  # 防止乱码
        writer = csv.writer(csvfile, dialect='excel')
        writer.writerow(
            ["約定日", "自己又は取次ぎの別", "顧客ID", "顧客名", '仮想通貨の名称', '売付け、買付け又は他の仮想通貨との交換の別', '仮想通貨の数量', '約定単価', '約定金額',
             '相手方の氏名又は名称', '取引に関して受け取る手数料、報酬そのほかの対価の額'])
        # 获取返回的数据
        result = get_order_match_result_data()
        r = 1
        # 遍历result中的每个元素。s
        for r in xrange(1, len(result)):
            # 对result的每个子元素作遍历
            row = result[r]
            f_symbol = row['f_symbol']
            currency = f_symbol[:-3]  # 币种
            f_type = row['f_type']
            if (f_type == 2) or (f_type == 4):
                f_type = '売付け'
            if (f_type == 1) or (f_type == 3):
                f_type = '買付け'
            f_filled_amount = row['f_filled_amount']
            f_price = row['f_price']
            f_user_id = row['f_user_id']
            writer.writerow([DateUtils.get_yesterday_format(), '自己', f_user_id,
                             '山田太郎', currency.upper(), f_type, f_filled_amount, f_price, f_filled_amount * f_price, '',
                             ''])

def closeCursor():
    # 关闭游标
    cursor.close()
    # 关闭连接
    conn.close()


write_date_to_csv()
