# -*- coding: utf-8 -*-
'''
func: 用于计算上市公司的 PE ratio
计算公式：每股收益。用年报当天的股价除以每股收益EPS能够得到PE ratio
'''

from Interface import *
from financial_config import *


def compute_PE_ratio(stock_price, published_date, eps, path):
    result={}
    for s in eps.keys():
        
        for y in eps[s].keys():
            #try:
                if s not in result.keys():
                    result[s]={}
                if s in published_date.keys() and y in published_date[s].keys():
                    if s not in stock_price.keys():
                        continue
                    date_str=published_date[s][y].rstrip("'").strip()
                    datelist=sorted(stock_price[s].keys())
                    if date_str not in stock_price[s].keys():
                        index=0
                        while(datelist[index]<date_str):
                            index +=1
    
                        if index >0:
                            date_str=datelist[index-1]
                        else:
                            date_str=datelist[0]
                            
                    if not isinstance(eps[s][y], float):
                        continue

                    price=float(stock_price[s][date_str])
    
                    if eps[s][y]==0:
                        print s, '\t', y, '\teps is zero------.'
                        result[s][y]=0
                    else:
                        PE_ratio=price/eps[s][y]
                        if PE_ratio<0:
                         
                            result[s][y]=0
                        else:
                            result[s][y]=PE_ratio
                    if s=='08137':
                        print s, '\t', y, '\t', ' PE_ratio: ', result[s][y]
            #except Exception:
                #print 'error:--- ', s, '\t', y
                #continue
    content=json.dumps(result, encoding='utf8', ensure_ascii=False)
    save_txt(content, path)
    return result


def Handle_PE_data():
    # 1. read_data
    EPS = json.loads(open(EPS_dict_path, 'r').read())
    stock_price = read_stock_price(stock_price_path)
    published_date = read_published_date(annual_report_published_date_path)

    # 2. compute
    PE_Ratio_dict=compute_PE_ratio(stock_price, published_date, EPS, PE_Ratio_dict_path)

    # 3. normalized the market capitalization
    normalized_data(PE_Ratio_dict, normalize_PE_Ratio_dict_path)

    # 4. compute delta market capitalization
    compute_delta_tone(PE_Ratio_dict, delta_PE_Ratio_dict_path)


if __name__=='__main__':
    Handle_PE_data()


