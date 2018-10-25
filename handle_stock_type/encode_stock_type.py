# -*- coding:UTF-8 -*-
"""
encode stock type and split stock list based on A and B
"""
import xlrd
import xlwt
import json


type_dict={
    'A':[1,0],
    'B':[0,1],
    'Basic Materials':[1,0,0,0,0,0,0,0,0,0],
    'Communications':[0,1,0,0,0,0,0,0,0,0],
    'Consumer, Cyclical':[0,0,1,0,0,0,0,0,0,0],
    'Consumer, Non-cyclical':[0,0,0,1,0,0,0,0,0,0],
    'Diversified':[0,0,0,0,1,0,0,0,0,0],
    'Energy':[0,0,0,0,0,1,0,0,0,0],
    'Financial':[0,0,0,0,0,0,1,0,0,0],
    'Industrial':[0,0,0,0,0,0,0,1,0,0],
    'Technology':[0,0,0,0,0,0,0,0,1,0],
    'Utilities':[0,0,0,0,0,0,0,0,0,1]
}


def read_cols(path, cols_list):
    wbk=xlrd.open_workbook(path)
    sheet=wbk.sheets()[0]

    data=[]
    for col in cols_list:
        data.append(sheet.col_values(col))
    return data


def save_txt(path, data_dict):
    f=open(path, 'w')
    f.write(data_dict)
    f.close()


def handle_dict(data):
    result_dict={}
    A_list=[]
    B_list=[]
    for i, v in enumerate(data[0]):
        if i==0 or len(v.strip())==0:
            continue
        key=str('%05d' %(int(v.strip('HK Equity').strip())))
        type_code=type_dict[data[1][i]]+type_dict[data[2][i]]
        result_dict[key]=type_code

        if data[1][i]=='A':
            A_list.append(key)
        elif data[1][i]=='B':
            B_list.append(key)
        else:
            print key, ' ========'

    save_txt('../interim_data/stock_list/OEE_stock_list.json', json.dumps(A_list, encoding='utf8', ensure_ascii=False))
    save_txt('../interim_data/stock_list/MPE_stock_list.json', json.dumps(B_list, encoding='utf8', ensure_ascii=False))
    return result_dict


def main():
    path='../interim_data/stock_type/AB_stocks_type_info_mod.xls'
    data_type_all=read_cols(path, [0,3,4])
    encoded_data=handle_dict(data_type_all)
    encoded_data=json.dumps(encoded_data)
    save_txt('../interim_data/stock_type/AB_stock_type_code.json', encoded_data)


if __name__=='__main__':
    main()


