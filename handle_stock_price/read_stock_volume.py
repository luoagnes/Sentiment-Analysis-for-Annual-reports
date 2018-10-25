#!-*- coding:utf8 -*-

import os
import xlrd
import json
import time
import csv

stock_list_path = '../interim_data/stock_list/AB_stock_list.json'
price_root_dir = '../ini_data/ini_stock_price/'
save_price_path = '../interim_data/stock_price/'
save_price_name = '/Volume.json'
print_date_path = '../interim_data/stock_price/all_kinds_volume_show.csv'

date_format1 = '%Y/%m/%d'
date_format2 = '%Y-%m-%d'


def read_csv(path):
    result = []
    fobj = open(path, "rb")
    read_f = csv.reader(fobj)
    for eachline in read_f:
        result.append(eachline)
    fobj.close()
    return result


def save_txt(content, path):
    if not os.path.exists(path):
        os.mkdir(path)
    f = open(path + save_price_name, 'w')
    f.write(content)
    f.close()


def read_excel(path):
    result = []

    wbk = xlrd.open_workbook(path)
    table = wbk.sheets()[0]
    nrows = table.norws

    for row in range(nrows):
        e = table.row_values(row)
        result.append(e)
    return result


def print_result(data_list, data_title_list, path):
    with open(path, "w") as csvfile:
        writer = csv.writer(csvfile)

        # 先写入columns_name
        writer.writerow(data_title_list)

        n = len(data_list)

        keys_list = list(map(lambda x: x.keys(), data_list))
        keys1 = list(set(reduce(list.__add__, keys_list)))
        print '---the length of stock is: ', len(keys1)
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


def change_date_str_fromat(my_str):
    '''
    function: switch string '01/10/2002 12:23:34' to '2002-10-01'
    str: the target date string
    format: such as '%d/%m/%Y %H:%M:%S'
    '''
    result_str = '#'
    if '-' in my_str:
        str_date = time.strptime(my_str, date_format2)

        year = str(str_date[0])
        month = '%02d' % str_date[1]
        day = '%02d' % str_date[2]
        result_str = '-'.join((year, month, day))
    elif '/' in my_str:
        str_date = time.strptime(my_str, date_format1)

        year = str(str_date[0])
        month = '%02d' % str_date[1]
        day = '%02d' % str_date[2]
        result_str = '-'.join((year, month, day))
    else:
        print ('You input string is: ', my_str, ' it is not a legal date string.')

    return result_str


def handle_price_data(data, index):
    result = {}

    for line in data[1:]:
        try:
            ini_date = line[0].strip('.HK').strip()
            date_str = change_date_str_fromat(ini_date)
            close_price = line[index]
            result[date_str] = close_price
        except Exception:
            print ('the error line is: ', line)
            continue

    return result


def main():
    all_result = []

    stock_list = json.loads(open(stock_list_path, 'r').read())

    price_kinds = os.listdir(price_root_dir)

    for price_data_dir in price_kinds:
        result = {}
        files = os.listdir(price_root_dir + price_data_dir + '/')

        index = 5
        if price_data_dir == 'new_stock_price':
            index = 6
        for f in files:
            if f.strip('.csv').strip() not in stock_list:
                print f, '---not in ----'
                continue
            print '===in: ', f
            stock = f.rstrip('.csv').strip()

            path = price_root_dir + price_data_dir + '/' + f
            data = read_csv(path)
            print f, '-----price kind name'
            result[stock] = handle_price_data(data, index)

        content = json.dumps(result, encoding='utf8', ensure_ascii=False)
        save_txt(content, save_price_path + price_data_dir)
        all_result.append(result)

    data_title_list = ['stock', 'date'] + price_kinds
    print_result(all_result, data_title_list, print_date_path)


if __name__ == '__main__':
    main()
