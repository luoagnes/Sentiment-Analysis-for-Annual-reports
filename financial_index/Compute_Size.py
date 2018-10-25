# -*- coding: utf-8 -*-
"""
size=log(market cap), i is the end of month before the filling date
data:
    1. the filling date
    2. compute the end of month before the filling date
    3. get volume of the date from database
    4. compute size
"""
import math
from financial_config import *
from Interface import *


def compute_volume_date(filling_date, save_path):
    """
    1. translate to date format
    2.get the month
    3.get the before month
    4.get the last day of the before month
    """
    volume_date={}
    index =0
   
    for s in filling_date.keys():
        index +=1
        
        volume_date[s]={}
        for y in range(2002, 2018):
            if str(y) not in filling_date[s].keys():
                continue

            date_str=filling_date[s][str(y)].strip(u"‘").strip(u"’").strip(u"'")
            
            if date_str=='' or date_str=='N/A' or date_str==None:
                continue

            date_list=[e for e in date_str.rstrip('\\n').split('-')]
            date_tuple=[int(e) for e in date_list]
            temp_tuple=(date_tuple[0], date_tuple[1], 1)
            time_str=switch_time(temp_tuple, -1)
            volume_date[s][str(y)]=['-'.join(date_list), time_str]

    save_json(volume_date, save_path)
    return volume_date
          

def find_outstanding(month, year,share_outstanding_dict):
    result=0
    m=''
    if month <7:
        m='6'
    else:
        m='12'

    if isinstance(share_outstanding_dict[year][m], float):
        result= share_outstanding_dict[year][m]
    else:
        while(year<2017):
            year +=1
            if isinstance(share_outstanding_dict[year]['6'], float):
                result= share_outstanding_dict[year]['6']
                break
            if isinstance(share_outstanding_dict[year]['12'], float):
                result= share_outstanding_dict[year]['12']
                break
    return result
        

def get_volume_and_price(volume_date_dict, volume_dict, stock_price_dict, save_path):
    """
    1. read the end of month before the filling date
    2. connect database
    3. query the volume
    4.save the volume
    """
    target_data_dict={}
    mis_data=[]

    for stock in volume_date_dict.keys():
        if stock not in volume_dict.keys():
            mis_data.append(stock+' have not volume data--')
            continue

        if stock not in stock_price_dict.keys():
            mis_data.append(stock + ' have not price data--')
            continue

        target_data_dict[stock]={}
        for year in volume_date_dict[stock].keys():
            target_date=volume_date_dict[stock][year][1]
            pub_date=volume_date_dict[stock][year][0]

            first_date=min(stock_price_dict[stock].keys())
            while target_date not in stock_price_dict[stock].keys():
                temp_tuple=[int(e) for e in target_date.split('-')]
                target_date=switch_time(temp_tuple, -1)

                if target_date<first_date:
                    break

            if target_date<first_date:
                mis_data.append(stock + ':'+year+':'+target_date+' have not price--')
                continue
            '''
            if target_date not in volume_dict[stock].keys():
                mis_data.append(stock + ':' + year + ':' + target_date + ' have not volume--')
                continue
            '''
            while target_date not in volume_dict[stock].keys():
                temp_tuple = [int(e) for e in target_date.split('-')]
                target_date = switch_time(temp_tuple, -1)

                if target_date < first_date:
                    break

            if target_date < first_date:
                mis_data.append(stock + ':' + year + ':' + target_date + ' have not volume--')
                break

            volume=volume_dict[stock][target_date]
            price=stock_price_dict[stock][target_date]
            target_data_dict[stock][year]=[price, volume]
    save_json(target_data_dict, save_path)
    return target_data_dict, mis_data


def compute_size(target_data_dict, save_path, mis_data):
    size_dict={}
    
    for s in target_data_dict.keys():
        size_dict[s]={}
        for y in target_data_dict[s].keys():
            '''
            a=target_data_dict[s][y][0]
            b=target_data_dict[s][y][1]
            print a, '\t', b, '  :ini--------'
            if not isinstance(a, float):
                a=float(a)
            if not isinstance(b, float):
                b=float(b)
            print a, '\t', b, '  :after--------'
            temp=0
            if isinstance(a, float) and isinstance(b, float):
                temp=a*b

            if temp==0 or temp<0:
                mis_data.append(s + ':' + y+ ' have not price-- a:'+str(a)+' b:'+str(b))
                continue

            print temp, ' ini size------'
            '''
            size_dict[s][y]=math.log(target_data_dict[s][y])
    save_json(size_dict, save_path)

    mis_path='/'.join(save_path.split('/')[:-1])+'/size_mis_data.txt'
    save_json(mis_data, mis_path)
    return size_dict

    
def Handle_Size_data():
    # 1. read data
    '''
    stock_price=json.loads(open(stock_price_path, 'r').read())
    filling_date = json.loads(open(annual_report_published_date_path, 'r').read())
    stock_volume=json.loads(open(stock_volume_path, 'r').read())

    # 2. get data
    save_path='../interim_data/Size_volume_date.txt'
    volume_date=compute_volume_date(filling_date, save_path)
    target_data_dict, mis_data=get_volume_and_price(volume_date, stock_volume, stock_price, save_path)
    '''
    # 3. compute
    target_data_dict=json.loads(open(Market_capitalization_dict_path,'r').read())
    mis_data=[]
    size_dict=compute_size(target_data_dict, Size_dict_path, mis_data)

    # 4. normalize
    normalized_data(size_dict, normalize_Size_dict_path)

    # 5. compute delta
    compute_delta_tone(size_dict, delta_Size_dict_path)


if __name__=='__main__':
    Handle_Size_data()
    print '--------------------Done----------------'
    

