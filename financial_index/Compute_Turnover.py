# -*- coding:utf-8 -*-
"""
turnover=log(the sum of volume(i-j))/outstanding(the filling date)
data:
    1. get the volume of the filling date and six to 252 trading days
    2. compute turnover
"""
import math
from financial_config import *
from Interface import *


def find_outstanding(month, year,share_outstanding_dict, flag):
    result=0
    m=''
    if month <7:
        m='6'
    else:
        m='12'

    nextm=str(18-int(m))
    byear=year
    ayear=year+1
    while(byear>=2002 and ayear<2019):
        if flag==1:
            print share_outstanding_dict.keys()
            print m, '\t', nextm, '\t', ayear, '\t', byear
            print share_outstanding_dict[str(byear)].keys()

        if m in share_outstanding_dict[str(byear)].keys():
            result = share_outstanding_dict[str(byear)][m]
            if flag==1:
                print byear, '\t', m, ':byear----in-------'
            break
        elif nextm in share_outstanding_dict[str(byear)].keys():
            result = share_outstanding_dict[str(byear)][nextm]
            if flag==1:
                print byear, '\t', nextm, ':byear----in-------'
            break
        else:
            if flag==1:
                print '---not in %d -----'% byear
            byear -=1

        if m in share_outstanding_dict[str(ayear)].keys():
            result = share_outstanding_dict[str(ayear)][m]
            if flag==1:
                print ayear, '\t', m, ':ayear----in-------'
            break
        elif nextm in share_outstanding_dict[str(ayear)].keys():
            result = share_outstanding_dict[str(ayear)][nextm]
            if flag==1:
                print ayear, '\t', nextm, ':ayear----in-------'
            break
        else:
            ayear +=1
            if flag==1:
                print '---not in %d -----' % ayear
    return result


def get_one_year_volume(pub_date, volume):
    volume_dict={}
    volume_list=[]

    date_tuple = [int(e.strip("‘".decode("utf8")).strip("’".decode("utf8"))) for e in pub_date.split('-')]
    for i in range(6, 253):
        time_str = switch_time(date_tuple, 0-i)
        if time_str in volume.keys():
            v=float(volume[time_str])
            volume_dict[time_str]=v
            volume_list.append(v)

    return volume_list, volume_dict
    

def get_data(ini_outstanding_dict, ini_volume_dict):
    volume_dict={}
    outstanding={}
    show_volume_dict={}

    filling_date = json.loads(open(annual_report_published_date_path, 'r').read())

    for s in filling_date.keys():

        if s not in ini_outstanding_dict.keys():
            #print '==========non stock in outstanding=========', s
            continue

        if s not in ini_volume_dict.keys():
            #print '###### non sotck in volume#######', s
            continue

        volume_dict[s]={}
        outstanding[s]={}
        show_volume_dict[s]={}
        for y in range(2002, 2018):
            year=str(y)

            if year not in ini_outstanding_dict[s].keys():
                #print '********non outstanding *******', s, year
                continue

            if year not in filling_date[s].keys():
                #print '---non filing date-----------', s, year
                continue

            pub_date=filling_date[s][year]
            one_volume_list, one_volume_dict=get_one_year_volume(pub_date, ini_volume_dict[s])

            date_tuple = [int(e.strip("‘".decode("utf8")).strip("’".decode("utf8")))  for e in pub_date.split('-')]
            if s=='00001':
                flag=1
            else:
                flag=0
            print '==============='
            one_share = find_outstanding(date_tuple[1], date_tuple[0], ini_outstanding_dict[s], flag)
            if one_share==0:
                if s=='00001':
                    print '-----share outstanding miss !!!----------', pub_date, date_tuple, date_tuple[1], date_tuple[0]
                    print s, y
                continue

            outstanding[s][year]=one_share
            volume_dict[s][year] = one_volume_list
            show_volume_dict[s][year]=one_volume_dict

    content=json.dumps(show_volume_dict)
    save_txt(content, '../interim_data/show_turnover_volume.txt')
    return outstanding, volume_dict

    
def compute_turnover(selected_volume, selected_outstanding, save_path):
    turnover_dict={}

    for s in selected_volume.keys():
        turnover_dict[s]={}
        for y in selected_volume[s].keys():

            a=sum(selected_volume[s][y])
            b=selected_outstanding[s][y]

            if a*b <=0:
                continue

            turnover_dict[s][y]=math.log(a/b)
            #print s, '\t', y, turnover_dict[s][y], '\t', a, '\t', b
    
    content=json.dumps(turnover_dict)
    save_txt(content, save_path)
    return turnover_dict


def Handle_turnover_data():
    # 1. 加载数据
    ini_volume_dict = json.loads(open(stock_volume_path, 'r').read())
    ini_Outstanding_dict= json.loads(open(Outstanding_dict_path, 'r').read())
    #print 'load data end---------'

    # 2. get volume and Outstanding
    outstanding, volume_dict=get_data(ini_Outstanding_dict, ini_volume_dict)
    #print '===get target volume and outstanding ----------'

    # 3. compute turnover
    Turnover_dict=compute_turnover(volume_dict, outstanding, Turnover_dict_path)
    #print 'compute turnover end ----------'

    # 4. normalize turnover
    normalized_data(Turnover_dict, normalize_Turnover_dict_path)

    # 5. compute delta value
    compute_delta_tone(Turnover_dict, delta_Turnover_dict_path)



if __name__=='__main__':
    Handle_turnover_data()