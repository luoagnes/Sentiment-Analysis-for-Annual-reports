# -*- coding: utf-8 -*-
import xlwt
import os
import csv
import json


def save_json(data,path):
    content=json.dumps(data)
    f=open(path, 'w')
    f.write(content)
    f.close()
    
    
def save_csv(path, data_dict):
     positive_list, negative_list=make_sure_word_order('word_dict/', '00041_2002')
     positive_list=[e.split('-')[0] for e in positive_list]
     negative_list=[e.split('-')[0] for e in negative_list]
     
     title=['stock', 'year', 'published_date', 'new_gradient', 'before_gradient', 'positive_sum', 'negative_sum']
     title.extend(positive_list)
     title.append('*****')
     title.extend(negative_list)
     
     with open(path, 'w') as f:
        writer = csv.writer(f,lineterminator='\n')
        fileHeader = title
        writer.writerow(fileHeader)
        
        for key0 in data_dict.keys():
            for key1 in data_dict[key0].keys():
                row_list=[key0, key1]
                row_list.extend(data_dict[key0][key1])
                writer.writerow(row_list)


def save_excel(path, data):
    wbk=xlwt.Workbook()
    ### -------------------------------
    table=wbk.add_sheet('count')
    table.write(0,0,'stock')
    table.write(0,1,'year')
    table.write(0,2,'published_date')
    table.write(0,3,'new_gradient')
    table.write(0,4,'before_gradient')
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
             
            col =col+2
            for e in data[key][year][:251]:
                col+=1
                table.write(row,col,e)
                
    wbk.save(path)


def make_sure_word_order(root, fname1):
    
    P1_path=root+'Positive/'+fname1+'_Positive.txt'
    P1_dict=json.loads(open(P1_path, 'r').read())
    positive_list=P1_dict.keys()
    
    N_path=root+'Negative/'+fname1+'_Negative.txt'
    N_dict=json.loads(open(N_path, 'r').read())
    negative_list=N_dict.keys()
    
    return positive_list, negative_list
    
    
def get_each_differnce(root, fname1, fname2, sentiment_list, flag):
    
    ### make sure the type of file
    sentiment_words='Negative'
    if flag==1:
        sentiment_words='Positive'
    else:
        sentiment_words='Negative'   
    
    P1_path=root+sentiment_words+'/'+fname1+'_'+sentiment_words+'.txt'
    P2_path=root+sentiment_words+'/'+fname2+'_'+sentiment_words+'.txt'
    P1_dict=json.loads(open(P1_path, 'r').read())
    P2_dict=json.loads(open(P2_path, 'r').read())   
    
    difference_list=[]
    for word in sentiment_list:
        difference_list.append(P2_dict[word]-P1_dict[word])
        
    return difference_list


def handle_first_year(root, f,P_sentiment_list, N_sentiment_list):
    
    ### ----base info----------------
    fname=f
        
    P_path=root+'Positive/'+fname+'_Positive.pkl'
    P_dict=json.loads(open(P_path, 'r').read())
    
    N_path=root+'Negative/'+fname+'_Negative.pkl'
    N_dict=json.loads(open(N_path, 'r').read())
    
    P_difference_list=[]
    for word in P_sentiment_list:
        P_difference_list.append(P_dict[word])
        
    N_difference_list=[]
    for word in N_sentiment_list:
        N_difference_list.append(N_dict[word])
    
    return P_difference_list, N_difference_list
    

def main():
    root='word_dict/'
    data={}
    file_list=os.listdir(root+'Positive/')
    
    published_date=json.loads(open('../result/AB_stocks_published_date_dict.txt','r').read())
    gradient_new=json.loads(open('../result/gradient_new.txt','r').read())
    gradient_before=json.loads(open('../result/gradient_before.txt','r').read())
    
    positive_list, negative_list=make_sure_word_order(root, '00001_2012')
    #print (sorted(file_list))
    
    P_difference_dict={}
    N_difference_dict={}
    
    for f2 in file_list:
        
        ### ----base info----------------
        f2=f2.strip()
        print f2
        print '----------------------'
        fname1=f2[:6]+str(int(f2[6:10])-1)
        fname2=f2[:10]
        stock=f2[:5]
        year=f2[6:10]
        print f2, '\t', fname1, '\t', fname2, '\t', stock, '\t', year
        if stock not in P_difference_dict.keys():
            P_difference_dict[stock]={}
            N_difference_dict[stock]={}
            
        if fname1+f2[10:] not in file_list:
            continue
            #P_difference_list, N_difference_list=handle_first_year(root, fname2,positive_list, negative_list)
        else:
        
            P_difference_list=get_each_differnce(root, fname1, fname2, positive_list, 1)
            N_difference_list=get_each_differnce(root, fname1, fname2, negative_list, 0)
            
            P_difference_dict[stock][year]=P_difference_list
            N_difference_dict[stock][year]=N_difference_list
            
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
            
       
            
        data[stock][year]=[p_date, new_gradient, before_gradient, sum(P_difference_list), sum(N_difference_list)]
        data[stock][year].extend(P_difference_list)
        data[stock][year].append('******')
        data[stock][year].extend(N_difference_list)
        
    save_json(P_difference_dict,'result/ab_positive_words_differ.txt') 
    save_json(N_difference_dict,'result/ab_negative_words_differ.txt') 
    
    save_csv('result/ab_differ_senti_words_count.csv', data)
    save_excel('result/differ_senti_words_count.xls', data)
        
if __name__=='__main__':
    main()
    

