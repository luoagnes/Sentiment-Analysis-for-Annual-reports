# -*- coding: utf-8 -*-
import xlwt
import os
import json


def save_excel(path, data):
    wbk=xlwt.Workbook()
    
    ### -------------------------------
    table=wbk.add_sheet('count')
    table.write(0,0,'stock')
    table.write(0,1,'year')
    table.write(0,2,'published_date')
    table.write(0,3,'ab_normal_return')
    table.write(0,4,'regression_coef')
    table.write(0,5,'Positive_words')
    table.write(0,6,'Negative_words')
    table.write(0,7,'Global_words')
    
    row=0
    col=0
    for key in data.keys():
       
        for year in data[key].keys():
            row +=1
            col=0
            table.write(row,col,key)
            table.write(row,col+1,year)
            table.write(row,col+2,data[key][year][0])
            table.write(row,col+3,data[key][year][1])
            table.write(row,col+4,data[key][year][2])
            table.write(row,col+5,data[key][year][3])
            table.write(row,col+6,data[key][year][4])
            
    wbk.save(path)
    
    
def print_each_doc(root, fname):
     
    P_path=root+'Positive/'+fname+'_Positive.txt'
    P_dict=json.loads(open(P_path, 'r').read())
    P=sorted(P_dict.iteritems(), key=lambda d:d[1], reverse=True)
    P=[d for d in P if d[1]>0]
    P_str=','.join(list(map(lambda x: x[0].split('-')[0] + ':'+ str(x[1]), P)))
    
    
    N_path=root+'Negative/'+fname+'_Negative.txt'
    N_dict=json.loads(open(N_path, 'r').read())
    N=sorted(N_dict.iteritems(), key=lambda d:d[1], reverse=True)
    N=[d for d in N if d[1]>0]
    N_str=','.join(list(map(lambda x: x[0].split('-')[0] + ':'+ str(x[1]), N)))
    
    G_path=root+'Global/'+fname+'_global_words.txt'
    G_dict=json.loads(open(G_path, 'r').read())
    G=sorted(G_dict.iteritems(), key=lambda d:d[1], reverse=True)
    G=[d for d in G if d[1]>0]
    G_str=','.join(list(map(lambda x: x[0].split('-')[0] + ':'+ str(x[1]), G)))
    
    return  P_str,  N_str, G_str
    

def main():
    root='word_dict/'
    data={}
    file_list=os.listdir(root+'Positive/')
    
    published_date=json.loads(open('../result/AB_stocks_published_date_dict.txt', 'r').read())  
    gradient_new=json.loads(open('../result/gradient_new.txt','r').read())
    gradient_before=json.loads(open('../result/gradient_before.txt','r').read())
    
    for f in file_list:
        fname=f[:10]
        stock=f[:5]
        year=f[6:10]
        P_str,  N_str, G_str=print_each_doc(root, fname)
        #print '------------successful!--------', fname
        p_date='#'
        new_gradient='#'
        before_gradient='#'
        
        if stock not in data.keys():
            data[stock]={}
        
        if stock in published_date.keys() and year in published_date[stock].keys():
            p_date=published_date[stock][year]
            
        if stock in gradient_new.keys() and year in gradient_new[stock].keys():
            new_gradient=gradient_new[stock][year]
            
        if stock in gradient_before.keys() and year in gradient_before[stock].keys():
            before_gradient=gradient_before[stock][year]
        
        data[stock][year]=[p_date, new_gradient, before_gradient, P_str,  N_str, G_str]
    save_excel('result/AB_DOC_senti_words.xls', data)
        
if __name__=='__main__':
    main()
    

