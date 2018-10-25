#!-*- coding:utf8 -*-

import json

def main():
    path='../interim_data/stock_type/AB_stock_type_code.json'
    data=json.loads(open(path, 'r').read())
    stock_list=data.keys()
    
    save_path='../interim_data/stock_list/AB_stock_list.json'
    f=open(save_path, 'w')
    content=json.dumps(stock_list)
    f.write(content)
    f.close()
	
if __name__=='__main__':
    main()