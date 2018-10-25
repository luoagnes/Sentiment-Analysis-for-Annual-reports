#!-*- coding:utf8 -*-
import xlwt
import xlrd
import json
import copy
import csv

result_path='result/all_model_result_norm.txt'


def traverse_dict(writer, data, write_data_list, row, col):
    if isinstance(data, dict):
        for key in data.keys():
            write_data_list.append(key)
            row, col=traverse_dict(writer, data[key], copy.deepcopy(write_data_list), row, col)
            write_data_list=write_data_list[:-1]
        return row, col
    else:
        if isinstance(data, list):
            line=write_data_list+data
            if isinstance(line, list):
                writer.writerow(line)
            print '----write over-------'
        else:
            write_data_list.append(data)

            if isinstance(write_data_list, list):
                writer.writerow(write_data_list)
            print '----write one over --------'

        return row, col


def print_result(data, path):

    '''
    data={
        'norm':{
            'oee':[12,12,45,30],
            'all':[13,13,46,31]},
        'delta':{
            'oee':[122,122,452,302],
            'all':[123,123,453,303]},
        'tone':{
            'oee':[123,123,453,303],
            'all':[133,133,463,313]}
    }

    wbk=xlwt.Workbook()
    table=wbk.add_sheet('sheet1')
    row=1
    col=0
    traverse_dict(table, data, [], row, col)
    wbk.save(path)
    '''
    file = open(path, 'wb')
    writer = csv.writer(file)
    row = 1
    col = 0
    traverse_dict(writer, data, [], row, col)


def compute_one_best_feature(data):
    result={}

    for model in data.keys():
        if model not in result.keys():
            result[model]={}

        vd_list=[0,0,0,0]
        fea_list=['','','','']
        for feature_com in data[model].keys():
            for i in range(4):
                if data[model][feature_com][i]>vd_list[i]:
                    vd_list[i]=data[model][feature_com][i]
                    fea_list[i]=feature_com

        result[model]['a']=fea_list[0]
        result[model]['p'] = fea_list[1]
        result[model]['r'] = fea_list[2]
        result[model]['f1'] = fea_list[3]

    return result


def compute_all_best_feature(data):
    final_result={}
    for data_kind in data.keys():
        if data_kind not in final_result.keys():
            final_result[data_kind]={}

        for stock_kind in data[data_kind].keys():

            result={}
            for feature_com in data[data_kind][stock_kind].keys():
                for model in data[data_kind][stock_kind][feature_com].keys():
                    if model not in result.keys():
                        result[model]={}

                    result[model][feature_com]=data[data_kind][stock_kind][feature_com][model]
            print result
            final_result[data_kind][stock_kind]=compute_one_best_feature(result)
    return final_result


def main():
    # 1. print data
    data = json.loads(open(result_path, 'r').read())
    path='result/all_result_tone_show.csv'
    print_result(data, path)

    # 2. compute best feature
    result=compute_all_best_feature(data)
    print result
    save_path='result/all_best_feature_tone_show.csv'
    print_result(result, save_path)


if __name__=='__main__':
    main()
