#!-*- coding:utf8 -*-

import os
import matplotlib
matplotlib.use('Agg')
import json


matplotlib.use('Agg')
days=250
price_path='../interim_data/stock_price/'
price_data_suffix='Close_Price.json'
published_date_path='../interim_data/annual_reports_published_date/AB_stocks_published_date_dict.txt'

save_return_path='Actual_return.json'
abnormal_return='Abnormal_return_for_'+str(days)+'_days.txt'


def save_txt(data, path):
    f=open(path, 'w')
    f.write(data)
    f.close()


def compute_return(stock_price, path):
    stock_return={}
    for s in stock_price.keys():
        datelist=sorted(stock_price[s].keys())
        stock_return[s]={}
        for i in range(1,len(datelist)):
            today=datelist[i]
            yeaterday=datelist[i-1]

            k=1
            while(float(stock_price[s][yeaterday])==0.0 and k<i):
                k+=1
                yeaterday=datelist[i-k]

            if k==i and float(stock_price[s][yeaterday])==0.0:
                continue

            return_value=round(float(stock_price[s][today])/float(stock_price[s][yeaterday])-1, 4)
            stock_return[s][today]=return_value
            print s, today, return_value
            print '------------------------'
    content=json.dumps(stock_return)
    save_txt(content, path)


def main():
    # 1. published date
    published_date=json.loads(open(published_date_path, 'r').read())

    # 2. stock price
    path=price_path+price_data_suffix
    stock_price=json.loads(open(path).read())

    # 3. compute actual return
    return_path=price_path+save_return_path
    compute_return(stock_price, return_path)
    print 'compute ', price_path, ' end !!-------'


if __name__=='__main__':
    main()
