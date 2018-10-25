# -*- coding: utf-8 -*-

import datetime
from sklearn import linear_model
import json
import xlwt
import os
import numpy

price_data_path='../interim_data/stock_price/'
published_date_path='../interim_data/annual_reports_published_date/AB_stocks_published_date_dict.txt'
result_path='../interim_data/Label/Gradient/'


### write excel
def write_dict_to_excel_3(path, data_dict, title):
    wbk=xlwt.Workbook()
    table=wbk.add_sheet('sheet1')
    
    ### write title
    col=0
    row=0
    for t in title:
        table.write(row, col, t)
        col +=1
    
    row=1
    col=0
    for key0 in data_dict.keys():
        
        for key1 in data_dict[key0].keys():
            
            table.write(row, col, key0)
            table.write(row, col+1, key1)
            try:
                table.write(row, col+2, data_dict[key0][key1])
            except Exception:
                table.write(row, col+2, data_dict[key0][key1].encode('utf-8'))
            row+=1
    wbk.save(path)
                
    
def encode_date(date_list):
	value_list=[]
	if len(date_list)==0:
		return value_list
	standard_date=datetime.datetime.strptime(date_list[0], '%Y-%m-%d')
	for date_str in date_list:
		current_date=datetime.datetime.strptime(date_str, '%Y-%m-%d')
		value=(current_date-standard_date).days
		value_list.append(value)
	return value_list


# %%% 4.regression and get a and b
def regression(X, Y):
	clf=linear_model.LinearRegression()
	clf.fit(X,Y)
	clf.predict(X)
	return clf.coef_[0][0], clf.predict(X)


def get_one_year_data(start_y, end_y, stock_price):
	X=[]
	Y=[]
	date_list=sorted(stock_price.keys())

	for d in date_list:
		if d>start_y and d<end_y:
			X.append(d)
			Y.append(float(stock_price[d]))
	X=encode_date(X)
	print ('the length of date is: ',len(X), ' ', len(Y))
	result=[X, Y]
	return result


def get_all_year_data(published_date, stock_price, path):
	result={}
	for s in published_date.keys():

		if s not in stock_price.keys():
			continue
		result[s]={}

		for y in published_date[s].keys():
			start_y=published_date[s][y]

			next_year=str(int(y)+1)
			if next_year in published_date[s].keys():
				end_y=published_date[s][next_year]

				result[s][y]=get_one_year_data(start_y, end_y, stock_price[s])
	content=json.dumps(result, encoding='utf8', ensure_ascii=False)
	f=open(path+'AB_all_years_data.txt', 'w')
	f.write(content.encode('utf8'))
	f.close()


def get_all_gradient(path):
	result={}
	data=json.loads(open(path+'AB_all_years_data.txt', 'r').read())
	for s in data.keys():
		result[s]={}
		for y in data[s].keys():
			d=data[s][y]
			#try:
			if len(d[0])==0:
				continue
			X=numpy.array(d[0]).reshape(len(d[0]), 1)
			Y=numpy.array(d[1]).reshape(len(d[1]), 1)

			b, _=regression(X, Y)
			result[s][y]=b
			'''
			except Exception:
				print '===regression error==: ', s, ':', y
				print len(d), len(d[0]), len(d[1])
				print X.shape, Y.shape
				print '=================================='
				return result
			'''
	return result

	
def save_result(result, path):
	if not os.path.exists(path):
		os.mkdir(path)

	content=json.dumps(result, encoding='utf8', ensure_ascii=False)
	f=open(path+'AB_gradients.txt', 'w')
	f.write(content.encode('utf8'))
	f.close()
	write_dict_to_excel_3(path+'AB_gradients.xls', result, ['code', 'year', 'gradients'])


def print_all_result():
	all_data=[]

	price_kinds=os.listdir(price_data_path)
	title=['stock', 'year']
	for price_dir_path in price_kinds:
		if price_dir_path.endswith('csv'):
			continue
		title.append(price_dir_path)
		
		price_path=result_path+price_dir_path+'/'
		gradient_file=price_path+'AB_gradients.txt'
		gradient_data=json.loads(open(gradient_file).read())
		all_data.append(gradient_data)

	all_save_data=[]
	n=len(all_data)
	stock_keys_list=list(map(lambda x:x.keys(), all_data))
	stock_keys=list(set(reduce(list.__add__, stock_keys_list)))
	for stock in stock_keys:
		year_keys_list=list(map(lambda x:x[stock].keys() if stock in x.keys() else [], all_data))
		year_keys=list(set(reduce(list.__add__, year_keys_list)))
		for year in year_keys:
			line=[stock, year]
			for i in range(n):
				if stock in all_data[i].keys() and year in all_data[i][stock].keys():
					line.append(str(all_data[i][stock][year]))
				else:
					line.append('#')
				
			all_save_data.append(line)

	wbk=xlwt.Workbook()
	table=wbk.add_sheet('sheet1')

	col=0
	row=0
	for til in title:
		table.write(row, col, til)
		col+=1

	row=1
	col=0
	for line in all_save_data:
		for e in line:
			table.write(row, col, e)
			col+=1
		row+=1
		col=0
	wbk.save(result_path+'gradient_compared.xls')


def main():

	## 1. stock list
	#stock_list=json.loads(open('../stock_list/result/AB_stock_list.txt', 'r').read())

	## 2. published date
	published_date=json.loads(open(published_date_path, 'r').read())


	## 3. stock price
	price_kinds=os.listdir(price_data_path)
	for price_dir_path in price_kinds:
		if price_dir_path.endswith('csv'):
			continue

		#price_path=price_data_path+price_dir_path+'/'
		price_path=price_data_path+'/'
		price_file=price_path+'Close_Price.json'
		stock_price=json.loads(open(price_file, 'r').read())

		## 4. get one year data
		get_all_year_data(published_date, stock_price, price_path)

		## 5. regression
		result=get_all_gradient(price_path)

		## 6. save data
		#save_result(result, result_path+price_dir_path+'/')
		save_result(result, price_data_path )
		break

	#print_all_result()


if __name__=='__main__':
	main()


