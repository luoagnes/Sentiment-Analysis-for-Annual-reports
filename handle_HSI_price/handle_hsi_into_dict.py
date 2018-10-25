# -*- coding: utf-8 -*-
import os
import xlrd
import xlwt
import json
import time
import csv  

HSI_price_path='../ini_data/ini_HSI_price/hsi.xlsx'      
#ini_price_path='../ini_data/ini_stock_price/hk_day_line_price/'
save_price_path='../interim_data/HSI_price/'
save_price_name='/Close_Price.json'


date_format1='%Y/%m/%d'
date_format2='%Y-%m-%d'

def read_csv(path):  
    result=[]
    fobj = open(path,"rb")  
    read_f = csv.reader(fobj)  
    for eachline in read_f:  
        result.append(eachline)
    fobj.close()
    return result
        
        
def save_txt(content, path):
    if not os.path.exists(path):
        os.mkdir(path)
    f=open(path+save_price_name, 'w')
    f.write(content)
    f.close()
    
    
def read_excel(path):
    result=[]
    
    wbk=xlrd.open_workbook(path)
    table=wbk.sheets()[0]
    nrows=table.nrows
    
    for row in range(nrows):
        e=table.row_values(row)
        result.append(e)
    return result		
	    

def change_date_str_fromat(my_str):
    '''
    function: switch string '01/10/2002 12:23:34' to '2002-10-01'
    str: the target date string
    format: such as '%d/%m/%Y %H:%M:%S'
    '''
    result_str='#'
    if '-' in my_str:
        str_date=time.strptime(my_str, date_format2)
        
        year=str(str_date[0])
        month='%02d' % str_date[1]
        day='%02d' % str_date[2]
        result_str='-'.join((year, month, day))
    elif '/' in my_str:
		str_date=time.strptime(my_str, date_format1)
		
		year=str(str_date[0])
		month='%02d' % str_date[1]
		day='%02d' % str_date[2]
		result_str='-'.join((year, month, day))
    else:
		print ('You input string is: ', my_str, ' it is not a legal date string.')
		
    return result_str
   

def handle_price_data(data, index):
    result={}
    
    for line in data[1:]:
        try:
            ini_date=line[0].split(',')[0].strip()
            date_str=change_date_str_fromat(ini_date)
            close_price=line[index]
            result[date_str]=close_price
        except Exception:
            print ('the error line is: ', line)
            continue
        
    return result


def main():
	data=read_excel(HSI_price_path)
	result=handle_price_data(data, 4)
		
	content=json.dumps(result, encoding='utf8', ensure_ascii=False)
	save_txt(content, save_price_path)

    

if __name__=='__main__':
    main()
    
    
        
        
        

