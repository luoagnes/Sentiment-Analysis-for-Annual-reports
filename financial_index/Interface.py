#! -*- coding:utf8 -*-

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
import datetime
import xlwt

def save_txt(content, path):
    f = open(path, 'w')

    if isinstance(content, unicode):
        content = content.encode('utf8')
    f.write(content)
    f.close()


def save_json(data, path):
    content=json.dumps(data, encoding='utf8', ensure_ascii=False)
    content=content.encode('utf8')

    save_txt(content, path)


def save_dict_to_excel(data, title, path):
    wbk=xlwt.Workbook()
    table=wbk.add_sheet('sheet1')

    row=0
    col=0
    for til in title:
        table.write(row, col, til)
        col+=1

    row=1
    col=0
    for k1 in data.keys():
        for k2 in data[k1].keys():
            table.write(row, col, k1)
            table.write(row, col+1, k2)
            col+=2
            if isinstance(data[k1][k2], list):
                for e in data[k1][k2]:
                    table.write(row, col, e)
                    col+=1

            else:
                table.write(row, col, data[k1][k2])
            row += 1
            col = 0
    wbk.save(path)


def read_content(path):
    content=json.loads(open(path, 'r').read())
    return content


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


def switch_time(time_tuple, interval):
    time_string = ''
    try:
        # d1 = time.strptime(time_str, '%Y-%m-%d')
        d2 = datetime.datetime(time_tuple[0], time_tuple[1], time_tuple[2])
        d3 = d2 + datetime.timedelta(days=interval)
        time_string = d3.strftime('%Y-%m-%d')
    except ValueError:
        print 'switch time error:---------------ValueError'
        time_string = '0-0-0'
    return time_string


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
        if s not in result.keys():
            result[s] = {}
        for y in data[s].keys():
            #i += 1
            min_v = min(sum_result[y])
            max_v = max(sum_result[y])
            if max_v==min_v:
                result[s][y]=1
            else:
                result[s][y] = (data[s][y] - min_v) / (max_v - min_v)

    if len(path.strip())>0:
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
    mis_data=[]
    for s in data.keys():
        if s not in result.keys():
            result[s] = {}
        for y in data[s].keys():
            before_y =str(int(y) - 1)

            if before_y not in data[s].keys():
                #print '---------not in -------------', before_y, s, type(before_y)
                mis_data.append(s+'\t'+before_y+'\thas not ini financial index data.')
                continue
            if isinstance(data[s][y], unicode) or isinstance(data[s][before_y], unicode):
                #print '----**** unicode not in ***-------'
                mis_data.append(s + '\t' + before_y + '\ttype is unicode and error.')
                continue
            if data[s][before_y] == 0:
                #print '========= zero ==============='
                mis_data.append(s + '\t' + before_y + '\tthe value is zero.')
                result[s][y] =0
                continue

            result[s][y] = data[s][y] - data[s][before_y]
    content = json.dumps(result, encoding='utf8', ensure_ascii=False)
    save_txt(content, path2)

    path3='/'.join(path2.split('/')[:-1])+'/mis_data_list.txt'
    save_json(mis_data, path3)
    return result

