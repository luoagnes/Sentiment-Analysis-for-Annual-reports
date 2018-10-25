# -*- coding: utf-8 -*-
import pickle
import csv
import xlwt
import os
import numpy
import datetime


def save_csv(path):
    data=pickle.load(open(path, 'r'))
    keys=data.keys()

    f=open(path+'.csv', 'w')
    writer=csv.writer(f)
    writer.writerow(['data', 'accuracy', 'precision', 'recall', 'F1'])
    for k in keys:
        writer.writerow([k]+data[k])
    f.close()


def save_excel(path, data):
    wbk=xlwt.Workbook()

    if isinstance(data, numpy.ndarray):
        data=numpy.ndarray.tolist(data)

    index=0
    for d in data:
        if isinstance(d, numpy.ndarray):
            d = numpy.ndarray.tolist(d)

        d=map(lambda x: numpy.ndarray.tolist(x) if isinstance(x, numpy.ndarray) else x, d)
        index +=1
        table=wbk.add_sheet('sheet'+str(index))

        col=0
        row=0
        table.write(row, col, 'stock')
        table.write(row, col+1, 'years')
        table.write(row, col+2, 'true_y')
        table.write(row, col+3, 'pred_y')

        for i,e in enumerate(d[0]):
            row +=1
            col=0
            table.write(row, col, d[2][i][0])
            table.write(row, col+1, d[2][i][1])
            table.write(row, col+2, str(e))
            table.write(row, col+3, d[1][i])
    wbk.save(path)

def save_result(root):
    files = os.listdir(root)
    # path='result/n_bow+before'
    for f in files:
        if '.xls' in f or '.csv' in f:
            continue
        #print f
        save_csv(root + f)
        
def print_final_result(result, path):
    wbk=xlwt.Workbook()
    sheet=wbk.add_sheet('sheet1')
    
    title=['method','accuracy', 'precision', 'recall', 'F1']
    col=0
    for e in title:
        sheet.write(0, col, e)
        col +=1
        
        
    row=1
    keys=sorted(result.keys())
    for k in keys:
        col=0
        sheet.write(row, col, k)
        for e in result[k]:
            col +=1
            sheet.write(row, col, e)
        row +=1
    wbk.save(path)
    
    
def read_pkl(path):
    return pickle.load(open(path, 'rb'))


def check_result_directory(path):
    temp=datetime.datetime.today()
    time_str=str(temp.month)+'_'+str(temp.day)+'_'+str(temp.hour)+'_'+str(temp.minute)
    root=path+time_str+'/'
    if not os.path.exists(root):
        os.mkdir(root)
    return root
    
    
    