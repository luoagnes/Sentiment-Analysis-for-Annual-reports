# -*- coding: utf-8 -*-
"""
用于整理计算后的金融指数，包括：
1. 获取数据
2. 调用相应的接口计算
3. 归一化
4. 计算delta tone
5. 保存数据
"""

import xlrd
import json


def save_txt(content, path):
    f = open(path, 'w')

    if isinstance(content, unicode):
        content = content.encode('utf8')
    f.write(content)
    f.close()


def read_data_from_excel(path):
    '''
    func: read data from excel and save according to the rows
    param:
        path: the path of which need to read
    return:
        a list, in which a row is a element
    '''
    result = []
    wbk = xlrd.open_workbook(path)
    table = wbk.sheets()[0]
    nrows = table.nrows

    for row in range(nrows):
        result.append(table.row_values(row))
    return result


def normalized_data(data, path):
    '''
    func: normalized data
    param: the data need to be normalized
    retrun:
        结果字典
    '''
    result = {}
    sum_result = {}
    for s in data.keys():
        for y in data[s].keys():
            if y not in sum_result.keys():
                sum_result[y] = []
            sum_result[y].append(data[s][y])
    i = 0
    for s in data.keys():
        for y in data[s].keys():
            if s not in result.keys():
                result[s] = {}
            i += 1
            min_v = min(sum_result[y])
            max_v = max(sum_result[y])
            result[s][y] = (data[s][y] - min_v) / (max_v - min_v)
    content = json.dumps(result, encoding='utf8', ensure_ascii=False)
    save_txt(content, path)
    return result


def read_stock_price(path):
    data = json.loads(open(path).read())
    return data


def read_published_date(path):
    data = json.loads(open(path).read())
    return data


def compute_delta_tone(data, path2):
    result = {}
    for s in data.keys():
        if s not in result.keys():
            result[s] = {}
        for y in data[s].keys():
            before_y = str(int(y) - 1)
            if before_y not in data[s].keys() or isinstance(data[s][y], unicode) or isinstance(data[s][before_y],                                                                             unicode):
                continue
            if data[s][before_y] == 0:
                continue
            result[s][y] = (data[s][y] - data[s][before_y]) / float(data[s][before_y])
    content = json.dumps(result, encoding='utf8', ensure_ascii=False)
    save_txt(content, path2)
    return result


