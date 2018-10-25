import os
import xlwt
import json

def write_excel(data, path):
    wbk=xlwt.Workbook()
    sheet=wbk.add_sheet('sheet1')
    
    col=0
    row=0
    for k1 in data.keys():
        
        for k2 in data[k1].keys():
            col=0
            sheet.write(row, col, k1)
            sheet.write(row, col+1, k2)
   
            if isinstance(data[k1][k2], list):
                col +=2
                for e in data[k1][k2]:
                    sheet.write(row, col, e)
                    col +=1
            elif isinstance(data[k1][k2], dict):
                col +=2
                keys=sorted(data[k1][k2].keys())
                for k3 in keys:
                    #sheet.write(row, col+2, k3)
                    if isinstance(data[k1][k2][k3], list):
                        col +=3
                        for h in data[k1][k2][k3]:
                            sheet.write(row, col, h)
                            col +=1
                    else:
                        sheet.write(row, col, data[k1][k2][k3])
                    col +=1
            else:
                sheet.write(row, col+2, data[k1][k2])
            row +=1
    wbk.save(path)

root='result/'

files=os.listdir(root)
#files=['all_financial_index_genera22.txt','all_financial_index_before.txt','all_financial_index_general1.txt']
#files=['../result/AB_stocks_published_date_dict.txt']
files=['all_financial_non_normal_non_BV_MC.txt', 'all_financial_non_normal.txt','general_turnover_dict.txt','all_financial_index_general.txt', 'normalized_size.txt','size.txt','all_financial_index_genera22.txt']
for f in files[:1]:
    #try:
        
    content=json.loads(open(root+f, 'r').read())
    write_excel(content, root+f[:-4]+'.xls')
        #content=json.loads(open(f, 'r').read())
        #write_excel(content, f[:-4]+'.xls')
        #if f=='normalized_size.txt':
            #print f, '  ----success !!!!!'

    #except Exception:
        #continue
    
    
