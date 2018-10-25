# -*- coding: utf-8 -*-
"""
func: 用于计算上市公司的 market Capitalization
计算公式：公司当年的 outstanding shares *  乘以年报当天的价格。
注意：Outstanding 2 (HK)  (1)&Outstanding 2 (HK) (2):用于计算Market Capitalization.
这两个文件要合并一下，各个股票每年6月和12月分别提取了outstanding shares的数目，乘以年报当天的价格就是Market Capitalization.
"""

import xlrd
import json
from financial_config import Outstanding_dict_path, stock_price_path, Market_capitalization_dict_path,\
                             normalize_Market_capitalization_dict_path, delta_Market_capitalization_dict_path,\
                             annual_report_published_date_path
from Interface import *


def find_outstanding(month, year,share_outstanding_dict):
    result=0
    m=''
    if int(month) <7:
        m='6'
    else:
        m='12'

    before_year=int(year)-1
    after_year=int(year)+1

    while(True):
        if year in share_outstanding_dict.keys():
            if m in share_outstanding_dict[year].keys():
                result=share_outstanding_dict[year][m]
                break
            elif str(18-int(m)) in share_outstanding_dict[year].keys():
                result=share_outstanding_dict[year][str(18-int(m))]
                break
            else:
                if before_year>=2002:
                    year=str(before_year)
                    before_year-=1
                elif after_year<2018:
                    year=str(after_year)
                    after_year+=1
                else:
                    break

    return result
    

def compute_market_capital(stock_price, published_date, outstanding_share):
    '''
    func: 计算 market capitalization
    param:
        stock_price: 股票价格
        published_date: 年报发行日期
        outstanding_share: 总股本
    return:
        market capitalization
    '''
    
    result={}
    j=0
    for s in outstanding_share.keys():
        result[s]={}
        
        for y in outstanding_share[s].keys():
            if s in published_date.keys() and y in published_date[s].keys():
                j +=1
                if s not in stock_price.keys():
                    continue
                date_str=published_date[s][y].strip(u"'").strip(u"‘").strip(u"’")
                datelist=sorted(stock_price[s].keys())
                if date_str not in stock_price[s].keys():
                    index=0
                    while(datelist[index]<date_str):
                        index +=1
                    if index >0:
                        date_str=datelist[index-1]
                    else:
                        date_str=datelist[0]

                if s=='01668' and y=='2009':
                    date_str='2009-09-30'

                price=stock_price[s][date_str]
                month=date_str.split('-')[1]
                
                tempy=y
                if s=='00700' and y=='2014':
                    month='12'
                    y='2013'

                cur_share=find_outstanding(month, y,outstanding_share[s])
                y=tempy

                capital=cur_share*float(price)

                result[s][y]=capital

    content=json.dumps(result, encoding='utf8', ensure_ascii=False)
    save_txt(content, Market_capitalization_dict_path)
    return result

    
def Handle_MCapital_data():
    # 1. read_outstanding_share
    outstanding_share = json.loads(open(Outstanding_dict_path, 'r').read())

    # 2. read_stock_price
    stock_price = read_stock_price(stock_price_path)

    # 3. read published date
    published_date = read_published_date(annual_report_published_date_path)

    # 4. compute market capitalization
    market_capital = compute_market_capital(stock_price, published_date, outstanding_share)

    # 5. normalized the market capitalization
    normalized_data(market_capital, normalize_Market_capitalization_dict_path)

    # 6. compute delta market capitalization
    compute_delta_tone(market_capital, delta_Market_capitalization_dict_path)


if __name__=='__main__':
    Handle_MCapital_data()
    print ('------end--------')


