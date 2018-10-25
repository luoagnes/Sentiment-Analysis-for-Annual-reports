# -*- coding: utf-8 -*-
"""
Votility: Standard deviation of the firm-specific com-
ponent of returns estimated using up to 60 months of
data as of the end of the month before the filing date.
We estimate volatility for all firms with at least 12
months of data during this 60-month period.

Votility=np.sqrt(252)*np.std(np.array(temp))

"""
import numpy as np
from financial_config import *
from Interface import *
       

def get_one_year_return(pub_date, return_dict):
    return_list=[]
    return_date_dict={}
    date_keys=return_dict.keys()

    for i in range(366):
        cur_date=switch_time(pub_date, i-365)
        if cur_date in date_keys:
            return_list.append(return_dict[cur_date])
            return_date_dict[cur_date]=return_dict[cur_date]
    return return_list, return_date_dict


def get_return_date(published_date_path, return_data):
    select_return_dict={}
    check_return_dict={}
    
    filling_date=json.loads(open(published_date_path,'r').read())
    for s in filling_date.keys():
        if s not in return_data.keys():
            continue

        select_return_dict[s]={}
        check_return_dict[s]={}
        for y in range(2002, 2018):
            year=str(y)
            
            if year not in filling_date[s].keys():
                continue

            date_str=filling_date[s][year].encode('utf8').strip("‘").strip("’")
            if date_str=='' or date_str=='N/A' :
                continue

            date_tuple=[int(e.strip("‘").strip("’")) for e in date_str.split('-')]
            return_list, return_date_dict=get_one_year_return(date_tuple, return_data[s])
            select_return_dict[s][year]=return_list
            check_return_dict[s][year]=return_date_dict

    content=json.dumps(check_return_dict)
    save_txt(content, '../interim_data/selected_return.txt')

    return select_return_dict
    
    
def compute_votility(select_return_dict, save_path):
    votility={}
    
    for s in select_return_dict.keys():
        votility[s]={}
        for y in select_return_dict[s].keys():
            '''
            date_list=stock_return[s].keys()

            temp=[]
            for i in range(365):
                date_tuple=[int(e) for e in return_date[s][y].strip().split('-')]
                date_str=switch_time(date_tuple, i)
                if date_str in date_list:
                    temp.append(stock_return[s][date_str])
                    if s=='01177' and y=='2004':
                        print date_str,'\t', temp[-1]
            if len(temp)==0:
                continue 
            
            v=max(temp) 
            n=temp.count(v)      
            temp= sorted(temp)[:-n]
            '''
            one_year_return=select_return_dict[s][y]
            if len(one_year_return)==0:
                print s, ':', y, '\t', one_year_return
                continue

            votility[s][y]=np.sqrt(252)*np.std(np.array(one_year_return))
            #print s, ':', y, '\t', votility[s][y]

    content=json.dumps(votility)
    save_txt(content, save_path)
    return votility


def Handle_Votility_data():
    # 1. 读取所有的股票return
    stock_return = json.loads(open(actual_return_path, 'r').read())

    # 2. 计算获取的return
    selected_return=get_return_date(annual_report_published_date_path, stock_return)

    # 3， 计算votility
    votility_dict=compute_votility(selected_return, Votility_dict_path)

    # 4.归一化
    normalized_data(votility_dict, normalize_Votility_dict_path)

    # 5.计算delta value
    compute_delta_tone(votility_dict, delta_Votility_dict_path)


if __name__=='__main__':
    Handle_Votility_data()