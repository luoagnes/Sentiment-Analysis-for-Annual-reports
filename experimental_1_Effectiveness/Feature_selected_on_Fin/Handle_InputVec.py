#!-*- coding:utf8 -*-
import os
import json
from itertools import combinations
feature_root_path='../../interim_data/financial_index/'
label_path='../../interim_data/stock_price/AB_gradients.txt'

ALL_stock_list_path='../../interim_data/stock_list/AB_stock_list.json'
MPE_stock_list_path='../../interim_data/stock_list/MPE_stock_list.json'
OEE_stock_list_path='../../interim_data/stock_list/OEE_stock_list.json'


def save_json(data, path):
    content=json.dumps(data, ensure_ascii=False, encoding='utf8')
    if isinstance(content, unicode):
        content=content.encode('utf8')

    f=open(path, 'w')
    f.write(content)
    f.close()


def save_input(data, path, name):
    if not os.path.exists(path):
        os.mkdir(path)

    invec_list=[]
    label_list=[]
    for one_vec in data:
        label=[1 if one_vec[-1]>0 else -1]
        invec=one_vec[:-1]

        invec_list.append(invec)
        label_list.append(label)

    invec_path=path+'inVec/'
    if not os.path.exists(invec_path):
        os.mkdir(invec_path)
    save_json(invec_list, invec_path+name+'.json')

    label_path = path + 'Label/'
    if not os.path.exists(label_path):
        os.mkdir(label_path)
    save_json(label_list, label_path + name + '.json')


def split_features(data_list, save_name, name_list):
    num_list=range(1,len(name_list))
    for i in range(1,len(num_list)+1):
        index_com_list=list(combinations(num_list, i))

        for index_com in index_com_list:
            new_data_list=[data_list[j] for j in index_com]
            name='_'.join([name_list[j] for j in index_com])

            new_data_list.append(data_list[0])
            split_data(new_data_list, save_name, name)


def split_data(data_list, save_name, name):
    ALL_stock_list = json.loads(open(ALL_stock_list_path, 'r').read())
    MPE_stock_list = json.loads(open(MPE_stock_list_path, 'r').read())
    OEE_stock_list = json.loads(open(OEE_stock_list_path, 'r').read())

    ALL_input = []
    MPE_input = []
    OEE_input = []

    stock_list = []
    for data_item in data_list:
        stock_list += data_item.keys()

    stock_list = list(set(stock_list))
    n = len(data_list)

    for stock in stock_list:
        for year in range(2002, 2018):
            one_vector = []
            for data_item in data_list:
                if stock not in data_item.keys():
                    break
                if not isinstance(data_item[stock], dict):
                    one_vector.append(data_item[stock])
                else:
                    if str(year) not in data_item[stock].keys():
                        break
                    else:
                        one_vector.append(data_item[stock][str(year)])

            if len(one_vector) < n:
                continue
            else:
                one_item = []
                for item in one_vector:
                    if isinstance(item, list):
                        one_item += item
                    else:
                        one_item.append(item)

                if stock in MPE_stock_list:
                    MPE_input.append(one_item)

                if stock in OEE_stock_list:
                    OEE_input.append(one_item)
                ALL_input.append(one_item)

    save_path1=save_name+'ALL/'
    save_input(ALL_input, save_path1, name)

    save_path2=save_name+'MPE/'
    save_input(MPE_input, save_path2, name)

    save_path3=save_name+'OEE/'
    save_input(OEE_input, save_path3, name)


def main():
    label=json.loads(open(label_path, 'r').read())
    # 1. 定位并读取因子
    files_list=os.listdir(feature_root_path)
    for dir_path in files_list:
        feature_path=feature_root_path+dir_path
        if os.path.isfile(feature_path):
            continue

        if dir_path!='financial_index_dict':
            continue
        data_list=[label]
        name_list=['#']
        feature_files_list=os.listdir(feature_path)
        for file_name in feature_files_list:
            path=feature_path+'/'+file_name
            feature_data=json.loads(open(path, 'r').read())
            data_list.append(feature_data)
            name_list.append(file_name.strip('.json'))

        save_path='InputVec/'+dir_path+'/'
        if not os.path.exists(save_path):
            os.mkdir(save_path)
        split_features(data_list, save_path, name_list)


if __name__=='__main__':
    main()