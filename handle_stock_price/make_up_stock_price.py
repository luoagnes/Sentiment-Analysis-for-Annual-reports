#!-*- coding:utf8 -*-
"""
1. 用new_stock_price 中的price 更新 hk_day_line_price_before中的price, 更新时只更新头和尾部的缺失
2. 用hk_day_line_price_before中的volume去更新new_stock_price 中的volume， 更新时交叉更新所有的volume
"""
import json


def update_price(new_price, before_price):
    """
    用new_stock_price 中的price 更新 hk_day_line_price_before中的price, 更新时只更新头和尾部的缺失
    :param new_price:
    :param before_price:
    :return:
    """
    for s in new_price.keys():
        if s not in before_price.keys():
            before_price[s]={}

        before_date_list=sorted(before_price[s].keys())
        new_date_list=sorted(new_price[s].keys())

        before_date_begin = '3'
        before_date_end = '3'
        if len(before_date_list)>0:
            before_date_begin = before_date_list[0]
            before_date_end = before_date_list[-1]

        if before_date_begin>new_date_list[0]:
            i=0
            while i<len(new_date_list) and new_date_list[i]<before_date_begin:
                if new_price[s][new_date_list[i]]==0:
                    continue
                before_price[s][new_date_list[i]]=new_price[s][new_date_list[i]]
                i+=1

        if before_date_end<new_date_list[-1]:
            i = -1
            while (0-i)<=len(new_date_list) and new_date_list[i]> before_date_end:
                if new_price[s][new_date_list[i]]==0:
                    continue
                before_price[s][new_date_list[i]] = new_price[s][new_date_list[i]]
                i -= 1
    return before_price


def update_volume(new_volume, before_volume):
    for s in new_volume.keys():
        if s not in before_volume.keys():
            continue

        new_date_list=new_volume[s].keys()
        before_date_list=before_volume[s].keys()

        for date_str in before_date_list:
            if date_str not in new_date_list:
                if float(before_volume[s][date_str])==0:
                    continue

                new_volume[s][date_str]=str(float(before_volume[s][date_str])*100)

    return new_volume


def save_json(data, path):
    content=json.dumps(data, ensure_ascii=False, encoding='utf8')
    f=open(path, 'w')

    if isinstance(content, unicode):
        content=content.encode('utf8')

    f.write(content)
    f.close()


def main():
    #new_price=json.loads(open('../interim_data/stock_price/new_stock_price/Close_Price.json', 'r').read())
    #before_price=json.loads(open('../interim_data/stock_price/hk_day_line_price/Close_Price.json', 'r').read())

    new_volume = json.loads(open('../interim_data/stock_price/new_stock_price/Volume.json', 'r').read())
    before_volume = json.loads(open('../interim_data/stock_price/hk_day_line_price/Volume.json', 'r').read())

    #before_price=update_price(new_price, before_price)
    #save_json(before_price, '../interim_data/stock_price/hk_day_line_price/Close_Price.json')

    new_volume=update_volume(new_volume, before_volume)
    save_json(new_volume, '../interim_data/stock_price/new_stock_price/Volume.json')


if __name__=='__main__':
    main()









