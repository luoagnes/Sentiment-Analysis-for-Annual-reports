# -*- coding: utf-8 -*-
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
                    sheet.write(row, col, str(e))
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
    

def print_data(*data):
    result={}
    
    keys1=data[0].keys()
    
    for s in keys1:
        result[s]={}
        for y in data[0][s].keys():
            result[s][y]=[]
            
            for t in data:
                if s in t.keys() and y in t[s].keys():
                    if isinstance(t[s][y], list):
                        result[s][y].extend(t[s][y])
                    else:
                        result[s][y].append(t[s][y])
                else:
                    result[s][y].append('#')
    
            
    write_excel(result, 'result/all_financial_and_grdients.xls')    
    
    
def main():
    gradient1_path='../result/gradient_new.txt'
    gradient2_path='../result/gradient_general.txt'
    gradient3_path='../result/gradient_before.txt'
    
    
    gradient1=json.loads(open(gradient1_path, 'r').read())
    gradient2=json.loads(open(gradient2_path, 'r').read())
    gradient3=json.loads(open(gradient3_path, 'r').read())
    
    financial_index_path='result/all_financial_non_normal.txt'
    financial_index=json.loads(open(financial_index_path, 'r').read())
    
    print_data(financial_index, gradient1, gradient2, gradient3)
    

if __name__=='__main__':
    main()



