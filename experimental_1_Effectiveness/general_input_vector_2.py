import json
from config import *


def save_json(data, path):
    content=json.dumps(data)
    f=open(path, 'w')
    f.write(content)
    f.close()


def save_input(input_data, path):
    X=[e[:-1] for e in input_data]
    Y=[[1 if e[-1]>0 else -1] for e in input_data]
    save_json(X, input_root_path+'input_vector/'+path+'_X.txt')
    save_json(Y, input_root_path+'label/'+path+'_Y.txt')


def pairs2(data_list, path_name):
    ALL_stock_list = json.loads(open(ALL_stock_list_path, 'r').read())
    MPE_stock_list = json.loads(open(MPE_stock_list_path, 'r').read())
    OEE_stock_list = json.loads(open(OEE_stock_list_path, 'r').read())

    ALL_input=[]
    MPE_input=[]
    OEE_input=[]

    stock_list=[]
    for data_item in data_list:
        stock_list+=data_item.keys()

    stock_list=list(set(stock_list))
    n=len(data_list)

    for stock in stock_list:
        for year in range(2002, 2018):
            one_vector=[]
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

            if len(one_vector)<n:
                continue
            else:
                one_item=[]
                for item in one_vector:
                    if isinstance(item, list):
                        one_item+=item
                    else:
                        one_item.append(item)

                if stock in MPE_stock_list:
                    MPE_input.append(one_item)

                if stock in OEE_stock_list:
                    OEE_input.append(one_item)
                ALL_input.append(one_item)

    save_input(ALL_input, 'ALL/ALL_'+path_name)
    save_input(MPE_input, 'MPE/MPE_' + path_name)
    save_input(OEE_input, 'OEE/OEE_' + path_name)


def general_dataset():
    # 1. load data
    tone_dict=json.loads(open(tone_dict_path, 'r').read())
    type_code_dict=json.loads(open(type_code_dict_path, 'r').read())
    fin_dict=json.loads(open(fin_dict_path, 'r').read())
    gradient_dict=json.loads(open(gradient_dict_path, 'r').read())

    path_name=''
    for senti in X_l1:
        for total_name in X_l2:
            for tone_kind in X_tone:
                for t in X_type:
                    for fin in X_financial:
                        X_data_list = []
                        path_name = senti+'_'+total_name+'_'
                        if isinstance(tone_kind, list):
                            for item in tone_kind:
                                X_data_list.append(tone_dict[senti][total_name][item])
                            path_name+=''.join(tone_kind)+'_'
                        elif len(tone_kind.strip()) > 0:
                            print tone_kind, '----tone kind---', type(tone_kind)
                            path_name+=tone_kind+'_'
                            X_data_list.append(tone_dict[senti][total_name][tone_kind])
                        else:
                            path_name+='null_'

                        if len(t.strip()) > 0:
                            path_name+='t_'
                            X_data_list.append(type_code_dict)
                        else:
                            path_name+='null_'

                        if len(fin.strip())>0:
                            X_data_list.append(fin_dict)
                            path_name+='fin'
                        else:
                            path_name+='null'

                        if len(X_data_list)==0:
                            pass

                        X_data_list.append(gradient_dict)
                        pairs2(X_data_list, path_name)


if __name__=='__main__':
    general_dataset()
