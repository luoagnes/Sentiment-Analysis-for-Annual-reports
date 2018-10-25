#！-*- coding:utf8 -*-
"""
处理最新的股价数据，问IP YP要的
"""
import os
import xlrd
import json
import time
import csv
import datetime

stock_list_path = '../interim_data/stock_list/AB_stock_list.json'
price_root_path = '../ini_data/ini_stock_price/data_vol.xlsx'
save_price_path = '../interim_data/stock_price/'
save_price_name = '/Volume.json'
print_date_path = '../interim_data/stock_price/all_kinds_Volume_show.csv'

date_format1 = '%Y/%m/%d'
date_format2 = '%Y-%m-%d'


def save_txt(content, path):
    if not os.path.exists(path):
        os.mkdir(path)
    f = open(path + save_price_name, 'w')
    f.write(content)
    f.close()


def read_excel(path):
    result = []

    wbk = xlrd.open_workbook(path)
    #table = wbk.sheet_by_name('Data')
    table=wbk.sheet_by_index(0)
    ncols = table.ncols

    for col in range(ncols):
        e = table.col_values(col)
        result.append(e)
    return result


def print_result(lastest, data_title_list, path):
    new=json.loads(open('../interim_data/stock_price/new_stock_price/Close_Price.json','r').read())
    before = json.loads(open('../interim_data/stock_price/hk_day_line_price_before/Close_Price.json', 'r').read())
    general = json.loads(open('../interim_data/stock_price/hk_day_line_price/Close_Price.json', 'r').read())
    data_list=[new, general, before, lastest]

    with open(path, "w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data_title_list)

        n = len(data_list)
        keys_list = list(map(lambda x: x.keys(), data_list))
        keys1 = list(set(reduce(list.__add__, keys_list)))
        data = []
        for stock in keys1:
            date_keys_list = list(map(lambda x: x[stock].keys() if stock in x.keys() else [], data_list))
            date_list = list(set(reduce(list.__add__, date_keys_list)))
            for date_line in date_list:
                line_content = [stock, date_line]

                for i in range(n):
                    try:
                        line_content.append(data_list[i][stock][date_line])
                    except Exception:
                        line_content.append('#')
                data.append(line_content)
        writer.writerows(data)


def timeStamp_to_str(interval):
    '''
    function: switch timeStamp to '2002-10-01'
    str: the target date string
    format: such as '%d/%m/%Y %H:%M:%S'
    '''
    d=datetime.datetime(1900, 1, 1)
    timeArray = d + datetime.timedelta(days=interval-2)
    date_str = timeArray.strftime("%Y-%m-%d")
    return date_str


def handle_price_data(data):
    result = {}
    print data[0][6:]
    date_list=[timeStamp_to_str(e) for e in data[0][6:]]
    print date_list
    for line in data[1:]:
        try:
            stock = '%05d' % int(line[3].strip(' HK Equity').strip())
            if stock not in result.keys():
                result[stock]={}

            for i, date_str in enumerate(date_list):
                close_price = line[i+6]
                print type(close_price)
                if isinstance(close_price, unicode) and close_price.strip()=='#N/A N/A':
                    continue
                result[stock][date_str] = close_price
        except Exception:
            print ('the error line is: ', line)
            continue

    return result


def main():
    all_result = []
    stock_list = json.loads(open(stock_list_path, 'r').read())

    data = read_excel(price_root_path)
    result = handle_price_data(data)

    content = json.dumps(result, encoding='utf8', ensure_ascii=False)
    save_txt(content, save_price_path)

    #data_title_list = ['stock', 'date', 'new', 'general','before', 'lastest']
    #print_result(result, data_title_list, print_date_path)


if __name__ == '__main__':
    main()