import xlwt
import os
import json

def save_excel(data):
	wbk=xlwt.Workbook()
	table=wbk.add_sheet('sheet1')
	
	col=0
	row=0
	for k in data.keys():
		col=0
		table.write(row, col, k)
		
		
		for d in sorted(data[k]):
			col +=1
			table.write(row, col, d)
		row +=1
        
	wbk.save('result/AB_chairman_published_Date_integrity.xls')


def main():
    published_date=json.loads(open('../result/AB_stocks_published_date_dict.txt','r').read())
    files=os.listdir('target_chairman_statement/')
    result={}

    for fname in files:
        stock=fname[:5]
        year=fname[6:10]

        if stock not in result.keys():
            result[stock]=[]
        
        if stock not in published_date.keys():
            result[stock].append(year+':#')
        elif year not in published_date[stock].keys():
            result[stock].append(year+':a')
        else:
            result[stock].append(year+': '+published_date[stock][year])


    save_excel(result)


if __name__=='__main__':
    main()
