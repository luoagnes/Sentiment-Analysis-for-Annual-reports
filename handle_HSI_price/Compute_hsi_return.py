#!-*- coding:utf8 -*-

import os
import matplotlib
matplotlib.use('Agg')
import datetime
import json
import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model

matplotlib.use('Agg')
days=250
hsi_price_path='../interim_data/HSI_price/Close_Price.json'

save_return_path='../interim_data/HSI_price/hsi_return.json'


def switch_time(date_str, interval):
    time_tuple=[int(e) for e in date_str.split('-')]
    time_string = ''
    try:
        #d1 = time.strptime(time_str, '%Y-%m-%d')
        d2 = datetime.datetime(time_tuple[0], time_tuple[1], time_tuple[2])
        d3 = d2 + datetime.timedelta(days=interval)
        time_string = d3.strftime('%Y-%m-%d')
    except ValueError:
        print 'switch time error:---------------ValueError'
        time_string = '0-0-0'
    return time_string


def save_txt(data, path):
	f=open(path, 'w')
	f.write(data)
	f.close()
	
	
def save_json(data, path):
    content=json.dumps(data)
    f=open(path, 'w')
    f.write(content)
    f.close()


def get_period_price(start_date, days, price_dict):
    date_list=sorted(price_dict.keys())
    
    start_price=0
    end_price=0
    for i, d in enumerate(date_list):
        if d >start_date:
            if i<1:
                i=1
            start_price=price_dict[date_list[i-1]]
            if i-1+days >len(date_list)-1:
                end_price=price_dict[date_list[-1]]
            else:
                end_price=price_dict[date_list[i-1+days]]
            break
    return start_price, end_price


def get_one_data(start_y, end_y, stock_price):
    X=[]
    Y=[]
    date_list=sorted(stock_price.keys())
    
    cnt=0
    for d in date_list:
        if d>start_y and cnt<days:
            X.append(d)
            Y.append(stock_price[d])
            cnt +=1
    X=encode_date(X)
    if len(X)==0:
        return [a]
    #print ('the length of date is: ',len(X))
    result=[X, Y]
    return result

    
def get_all_data(published_date, stock_price):
    result={}
    for s in published_date.keys():
        result[s]={}
        for y in published_date[s].keys():
            start_date=published_date[s][y]

            end_date=switch_time(start_date, days)

            if s not in stock_price.keys():
                continue
            data=get_one_data(start_date, end_date, stock_price[s])
            if len(data)==0:
                continue
            result[s][y]=data
    return result
	
def compute_return(stock_price, path):
	stock_return={}

	
	datelist=sorted(stock_price.keys())
	for i in range(1,len(datelist)):
		today=datelist[i]
		yeaterday=datelist[i-1]
		
		k=1
		while(float(stock_price[yeaterday])==0.0 and k<i):
			k+=1
			yeaterday=datelist[i-k]
		
		if k==i and float(stock_price[yeaterday])==0.0:
			continue
		
		return_value=round(float(stock_price[today])/float(stock_price[yeaterday])-1, 4)
		stock_return[today]=return_value
		print  today, return_value
		print '------------------------'
	content=json.dumps(stock_return)
	save_txt(content, path)


def main():
	# 2. stock price
	stock_price=json.loads(open(hsi_price_path).read())
	
	# 3. compute actual return
	compute_return(stock_price, save_return_path)
			


if __name__=='__main__':
    main()
