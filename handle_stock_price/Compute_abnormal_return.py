#!-*- coding:utf8 -*-

import os
import datetime
import time
import json
import matplotlib


matplotlib.use('Agg')
days=250
return_dir_path='../interim_data/stock_price/'
return_data_suffix='Actual_return.json'
published_date_path='../interim_data/annual_reports_published_date/AB_stocks_published_date_dict.txt'

hsi_return_path='../interim_data/HSI_price/hsi_return.json'
abnormal_return_suffix='Abnormal_return_for_'+str(days)+'_days.txt'


def Caltime(date1,date2):
	date1=time.strptime(date1,"%Y-%m-%d")
	date2=time.strptime(date2,"%Y-%m-%d")

	date1=datetime.datetime(date1[0],date1[1],date1[2])
	date2=datetime.datetime(date2[0],date2[1],date2[2])
	return (date2-date1).days


def switch_time(date_str, interval):
	time_tuple=[int(e) for e in date_str.split('-')]
	time_string = ''
	try:
		d2 = datetime.datetime(time_tuple[0], time_tuple[1], time_tuple[2])
		d3 = d2 + datetime.timedelta(days=interval)
		time_string = d3.strftime('%Y-%m-%d')
	except ValueError:
		print 'switch time error:---------------ValueError'
		time_string = '0-0-0'
	return time_string


def save_json(data, path):
	content=json.dumps(data)
	f=open(path, 'w')
	f.write(content)
	f.close()


def get_period_price(start_date, end_date, return_dict):
	date_list=sorted(return_dict.keys())

	return_list=[0]*days
	for date_item in date_list:
		if date_item >=start_date and date_item<end_date:
			d=Caltime(start_date,date_item)
			return_list[d]=return_dict[date_item]

	return return_list
	

def compute_abnormal_return(published_date, stock_return, hsi_return):
	result={}
	for s in published_date.keys():
		result[s]={}
		for y in published_date[s].keys():
			start_date=published_date[s][y]
			if s not in stock_return.keys():
				continue
			return_dict=stock_return[s]
			end_date=switch_time(start_date, days)
			
			stock_return_list=get_period_price(start_date, end_date, return_dict)
			hsi_return_list=get_period_price(start_date, end_date, hsi_return)
			
			return_list=zip(stock_return_list, hsi_return_list)
			ab_return=round(sum(list(map(lambda x:x[0]-x[1], return_list))),4)

			result[s][y]=ab_return
	return result


def main():

	# 1. published date
	published_date=json.loads(open(published_date_path, 'r').read())

	# 2. hsi return
	hsi_return=json.loads(open(hsi_return_path).read())

	return_kinds_list=os.listdir(return_dir_path)
	for return_path in return_kinds_list:
		if return_path.endswith('.csv'):
			continue
		path=return_dir_path+return_path+'/'+return_data_suffix
		# 3. stock return
		stock_return=json.loads(open(path).read())
		
		# 4. compute abnormal return
		ab_return_path=return_dir_path+return_path+'/'+abnormal_return_suffix
		ab_return=compute_abnormal_return(published_date, stock_return, hsi_return)
		save_json(ab_return,ab_return_path)
		print return_path, ' compute end ----'


if __name__=='__main__':
	main()
