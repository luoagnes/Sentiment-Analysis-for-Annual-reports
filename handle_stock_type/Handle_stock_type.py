# -*- coding:UTF-8 -*-
import xlrd
import xlwt

def read_cols(path, cols_list):
	wbk=xlrd.open_workbook(path)
	sheet=wbk.sheets()[0]
	
	data=[]
	for col in cols_list:
		data.append(sheet.col_values(col))
	return data


def handle_dict(data):
	result_dict={}
	for i, v in enumerate(data[0]):
		temp=list(map(lambda x: x[i], data[1:]))
		result_dict[v]=temp
	return result_dict
		

def merge_data(A, B):
    result={}
    for k in A.keys():
        if k in B.keys():
            result[k]=A[k]+B[k]
        else:
            result[k]=A[k]
    return result

def save_excel(data):
	wbk=xlwt.Workbook()
	table=wbk.add_sheet('sheet1')
	table.write(0, 0, 'stock')
	table.write(0, 1, 'C_name')
	table.write(0, 2, 'name')
	table.write(0, 3, 'AB_type')
	table.write(0, 4, 'General_type')
	
	col=0
	row=1
	for k in data.keys():
		col=0
		table.write(row, col, k)
		
		for d in data[k]:
			col +=1
			table.write(row, col, d)
		row +=1
        
	wbk.save('../interim_data/stock_type/AB_stocks_type_info_mode.xls')
	wbk.save('../interim_data/stock_type/AB_stocks_type_info.xls')
	
		
if __name__=='__main__':
	path1='../ini_data/ini_stock_type/List-with sector.xls'
	path2='../ini_data/ini_stock_type/stock listAB.xlsx'
	
	data_type_general=read_cols(path1, [0,2])
	data_type_AB=read_cols(path2, [0,1,2,9])

	general_type=handle_dict(data_type_general)
	AB_type=handle_dict(data_type_AB)

	result=merge_data(AB_type, general_type)
	save_excel(result)
	print '-----done----------'


