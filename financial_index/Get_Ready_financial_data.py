# -*- coding: utf-8 -*-
from financial_config import *
from Interface import *


def read_financial_data(path, path2, flag):
    result={}
    
    # 1. read data from excel
    data=read_data_from_excel(path)

    # 2. handle data into a dict
    for line in data[1:]:
        
        stock=line[0].strip('.HK').strip()
        
        if len(stock.strip())==0:
            continue

        if not stock.isdigit():
            continue
        stock='%05d' % int(stock)
        result[stock]={}

        for y in range(2002, 2018):
            v=''
            if flag==2:
                v=line[y-1995]
            else:
                v=line[y-2000]
            
            if not isinstance(v, float):
                if '--' in v:
                    continue
              
                v=float(v.replace(',','')) 
            if flag==0 and v<0:
                continue
            
            result[stock][str(y)]=v
            
    content=json.dumps(result, encoding='utf8', ensure_ascii=False)
    save_txt(content, path2)
    return result


def handle_cell_value(e, result, stock, year, month):
    if not isinstance(e, float):
        e=e.replace(',','')
        if '--' in e:
            pass
        else:
            result[stock][year][month]=float(e)
    else:
        result[stock][year][month]=e

    
def read_Outsatnding(path, path2):
    result={}
    
    # 1. read data from excel
    data=read_data_from_excel(path)

    # 2. handle data into a dict
    for line in data[1:]:
        
        stock=line[0].strip('.HK').strip()
        
        if len(stock.strip())==0:
            continue

        if not stock.isdigit():
            continue
        stock='%05d' % int(stock)
        result[stock]={}
        
        k=1
        for y in range(2002, 2018):
            result[stock][str(y)]={}

            v1=line[y-2000+k-1]
            handle_cell_value(v1, result, stock, str(y), '6')

            v2=line[y-2000+k]
            handle_cell_value(v2, result, stock, str(y), '12')
            k+=1

    content=json.dumps(result, encoding='utf8', ensure_ascii=False)
    save_txt(content, path2)
    return result


def main():
    ROE_Diluted=read_financial_data(ini_ROE_Diluted_path, ROE_Diluted_dict_path,1)
    norm_ROE_Diluted=normalized_data(ROE_Diluted, normalize_ROE_Diluted_dict_path)
    compute_delta_tone(ROE_Diluted, delta_ROE_Diluted_dict_path)

    BPS=read_financial_data(ini_BPS_path, BPS_dict_path,1)
    norm_BPS=normalized_data(BPS, normalize_BPS_dict_path)
    compute_delta_tone(BPS, delta_BPS_dict_path)

    Outstanding=read_Outsatnding(ini_Outstanding_path, Outstanding_dict_path)
    # norm_Outstanding=normalized_data(Outstanding, normalize_Outstanding_dict_path)
    # compute_financial_tone(norm_Outstanding, delta_Outstanding_dict_path)

    EPS=read_financial_data(ini_EPS_path, EPS_dict_path,1)
    norm_EPS=normalized_data(EPS, normalize_EPS_dict_path)
    compute_delta_tone(EPS, delta_EPS_dict_path)

    Equity_Multiplier=read_financial_data(ini_Equity_Multiplier_path, Equity_Multiplier_dict_path,1)
    norm_Equity_Multiplier=normalized_data(Equity_Multiplier, normalize_Equity_Multiplier_dict_path)
    compute_delta_tone(Equity_Multiplier, delta_Equity_Multiplier_dict_path)

    Book_Value=read_financial_data(ini_Book_Value_path, Book_Value_dict_path,1)
    norm_Book_Value=normalized_data(Book_Value, normalize_Book_Value_dict_path)
    compute_delta_tone(Book_Value, delta_Book_Value_dict_path)


if __name__=='__main__':
    main()
   




