# -*- coding: utf-8 -*-
import numpy
import pickle
from config import *
from sklearn.model_selection import KFold
from file_operation import *
from test_performance import get_performance_parameters
from model import * 
import json

def split_dataset(X, Y, stocks_years_flag):
    X[X=='#']=0
    X[X=='-inf']=0
    X=X.astype(numpy.float64)
    Y[Y==0]=1    
    if numpy.isnan(X).any():
        #X.dropna(inplace=True)
        X[numpy.isnan(X)]=0
        #X[X==numpy.NAN]=0
    X=X  #[:,-21:]
    kf = KFold(n_splits=4)
    DataSet=[]
    for train, test in kf.split(X):
        #DataSet.append([X[train],  X[test], Y[train],Y[test]])
        DataSet.append([X[train],  X[test], Y[train],Y[test], stocks_years_flag[train], stocks_years_flag[test]])
    return DataSet


def one_model(dataset, path, method_name, method):
    
    method_train=[]
    method_test = []
    
    print_result={}
    train_print = []
    test_print = []
    
    for samples in dataset:
        
        train_flag=samples[4]
        test_flag=samples[5]
        samples=samples[:4]  #samples[:-2]
        #print samples[0].shape
        #print '-------------- above is the shape of input vector -------------'
        test_pred, train_pred=method(*samples)
        #print '---------- linear 2 is success ----------------'
        a=test_pred.shape[0]
        test_pred.shape=(a,1)
        b=train_pred.shape[0]
        train_pred.shape=(b,1)

        train = get_performance_parameters(samples[2], train_pred)
        test = get_performance_parameters(samples[3], test_pred)

        temp_train=numpy.hstack((train_flag, samples[2],train_pred))
        temp_test=numpy.hstack((test_flag, samples[3],test_pred))
        
        #print temp_train.shape
        #print temp_test.shape
        train_print.append(temp_train.tolist())
        test_print.append(temp_test.tolist())
        method_train.append(train)
        method_test.append(test)
        break
    #print len(train_print), len(train_print[0]), '\t', len(train_print[0][0]), '\t', type(train_print[0][0][0])
    #print numpy.array(train_print).shape
    print_result['train']=numpy.array(train_print)
    print_result['test']=numpy.array(test_print)
    #save_excel(path+'_'+method_name+'_train.xls', train_print)
    #save_excel(path+'_'+method_name+'_test.xls', test_print)
    
    LR_train=numpy.array(method_train).mean(axis=0)
    LR_test=numpy.array(method_test).mean(axis=0)
    
    return list(LR_train), list(LR_test), print_result

 
def model(dataset, path):
    result={}
    result_print={}
   
    train_result, test_result, print_result=one_model(dataset, path, 'LR', test_LogisticRegression)
    result['LR_train']= train_result
    result['LR_test'] = test_result
    result_print['LR']=print_result
    
    train_result, test_result, print_result=one_model(dataset, path, 'DT', test_DecisionTreeClassifier)
    result['DT_train'] =  train_result
    result['DT_test'] =  test_result
    result_print['DT']=print_result
    
    train_result, test_result, print_result=one_model(dataset, path, 'RF', test_RandomForestClassifier)
    result['RF_train'] =  train_result
    result['RF_test'] =  test_result
    result_print['RF']=print_result
    
    train_result, test_result, print_result=one_model(dataset, path, 'SVC_rbf', test_SVC_rbf)
    result['SVC_rbf_train'] =  train_result
    result['SVC_rbf_test'] =  test_result
    result_print['SVC_rbf']=print_result
 
    train_result, test_result, print_result=one_model(dataset, path, 'SVC_linear', test_SVC_linear)
    result['SVC_linear_train'] =  train_result
    result['SVC_linear_test'] =  test_result
    result_print['SVC_linear']=print_result
    
    #train_result, test_result=one_model(dataset, path, 'SVC_poly', test_SVC_poly)
    #result['SVC_polynorm_train'] =  train_result
    #result['SVC_polynorm_test'] =  test_result

    train_result, test_result, print_result=one_model(dataset, path, 'SVC_sig', test_SVC_sig)
    result['SVC_sigmoid_train'] =  train_result
    result['SVC_sigmoid_test'] =  test_result
    result_print['SVC_sigmoid']=print_result
    
    ## -------------------test define kernel method ------------###
    '''
    train_result, test_result, print_result=one_model(dataset, path, 'SVC_rbf', test_SVC_rbf2)
    result['SVC_rbf_train'] =  train_result
    result['SVC_rbf_test'] =  test_result
    result_print['SVC_rbf']=print_result
    
    train_result, test_result, print_result=one_model(dataset, path, 'SVC_linear2', test_SVC_linear2)
    result['SVC_linear_train'] =  train_result
    result['SVC_linear_test'] =  test_result
    result_print['SVC_linear']=print_result
    '''
    #train_result, test_result=one_model(dataset, path, 'SVC_poly', test_SVC_poly)
    #result['SVC_polynorm_train'] =  train_result
    #result['SVC_polynorm_test'] =  test_result
    '''
    train_result, test_result, print_result=one_model(dataset, path, 'SVC_sig', test_SVC_sig2)
    result['SVC_sigmoid_train'] =  train_result
    result['SVC_sigmoid_test'] =  test_result
    result_print['SVC_sigmoid']=print_result
    '''
    ##----------------------------over-------------------------####

    train_result, test_result, print_result=one_model(dataset, path, 'GNB', test_GaussianNB)
    result['GNB_train'] =  train_result
    result['GNB_test'] =  test_result
    result_print['GNB']=print_result
    
    
    '''
    train_result, test_result=one_model(dataset, path, 'MNB', test_MultinomialNB)
    result['MNB_train'] =  train_result
    result['MNB_test'] =  test_result
    '''
    
    
    train_result, test_result, print_result=one_model(dataset, path, 'BNB', test_BernoulliNB)
    result['BNB_train'] =  train_result
    result['BNB_test'] =  test_result
    result_print['BNB']=print_result
    
    #print_final_result(result, 'result/121521/MPE/'+path+'_sum_result.xls')
    return result, result_print

def compute_accuracy(data_array, type_dict, index, flag):
    
    data=data_array.tolist()
    true_num={}
    sum_num={}   
    result={}
    if flag=='year':
         for dataset in data:
           for d in dataset:
               y=d[1]
               stock=d[0]
               
               if y not in true_num.keys():
                   true_num[y]={}
                   sum_num[y]={}
               if stock in type_dict.keys():
                   type_name=type_dict[stock][1]
                   if type_name not in true_num[y].keys():
                       true_num[y][type_name]=0
                       sum_num[y][type_name]=0
                   
               sum_num[y][type_name] +=1
               if d[2]==d[3]:
                   true_num[y][type_name] +=1

         for y in true_num.keys():
             result[y]={}
             for t in true_num[y].keys():
                 result[y][t]=true_num[y][t]/float(sum_num[y][t])
         return result

    elif flag=='code':
        for dataset in data:
           for d in dataset:
               y=d[0]

               if y not in true_num.keys():
                   true_num[y]={}
                   sum_num[y]={}

               if y in type_dict.keys():
                   type_name=type_dict[y][1]
                   if type_name not in true_num[y].keys():
                       true_num[y][type_name]=0
                       sum_num[y][type_name] =0

               sum_num[y][type_name] +=1
               if d[2]==d[3]:
                   true_num[y][type_name] +=1

        for y in true_num.keys():
            result[y]={}
            for t in true_num[y].keys():
                result[y][t]=true_num[y][t]/float(sum_num[y][t])
        return result

    else:

        for dataset in data:
            for d in dataset:
                stock=d[0]
           
                if stock in type_dict.keys():
                    type_name=type_dict[stock][index]
                    if type_name not in true_num.keys():
                        true_num[type_name]=0
                        sum_num[type_name]=0
                    sum_num[type_name] +=1
                    if d[2]==d[3]:
                        true_num[type_name] +=1
    
    for t in true_num.keys():
        result[t]=true_num[t]/float(sum_num[t])
    return result
 

def print_result_data(result_print, type_name_dict, index, name, flag):
    result={}

    for m in result_print.keys():
        result[m]={}

        train=result_print[m]['train']
        test=result_print[m]['test']
        
        result[m]['train']=compute_accuracy(train, type_name_dict, index, flag)
        result[m]['test']=compute_accuracy(test, type_name_dict, index, flag)
    
    content=json.dumps(result)
    f=open('result/121521/ALL/'+name+'_count_result.txt', 'w')
    f.write(content)
    f.close()
    return result
        
'''
def read_input_data():
    X=[]
    Y=[]

    for path in x_path_list+x_type_path_list+x_financial_path_list:
        X.append(read_json(path))
        
    for path in y_path_list:
        Y.append(read_json(path))
    
    return X,Y
'''

#def switch_dict(data_dict):
        
def save_all(data, path):
    wbk=xlwt.Workbook()
    sheet=wbk.add_sheet('sheet1')
    
    col=0
    row=0
    for d in data:
        for e in d:
            sheet.write(row, col, e)
            col +=1
        row+=1
    wbk.save(path)

                    
def main():
    #root=check_result_directory(result_directory)
    result={}
    #X, Y=read_input_data()
    
    stocks_years_flag=numpy.array(json.loads(open(root+years_flag_path, 'r').read()))
    type_name_dict=json.loads(open(type_flag_path, 'r').read())

    for i,k1 in enumerate(x_data_name_l1):
        #k1='Negative'
        k1_=k1
        k2_=''
        k3_=''
        if len(k1.strip())==0:
            result['null']={}
            result['null']['null']={}
            result['null']['null']['null']={}
            
            k1_='null'
            k2_='null'
            k3_='null'
        else:
            result[k1]={}
        for j,k2 in enumerate(x_data_name_l2):
            #k2='total'
            if len(k2.strip())>0 and len(k2_.strip())==0:
                k2_=k2
                result[k1_][k2_]={}
            for h,k3 in enumerate(x_data_name_l3):
                #k3=['1', '2', '3']
                X=[]
                if len(k1.strip())==0:
                    k3_='null'
                else:
                    k3_=''
                
                if len(k3_.strip())==0:
                    if (not isinstance(k3, list)) and len(k3.strip())==0:
                        k3_='null'
                    elif isinstance(k3, list):
                        k3_='_'.join(k3)
                        for k3_e in k3:
                            t=numpy.array(json.loads(open(root+'X_'+k1+'_'+k2+'_'+k3_e+'.txt', 'r').read()))
                            if isinstance(X, list):
                                a=numpy.array(t).shape[0]
                                X=numpy.empty((a,0))
                            X=numpy.hstack((X,numpy.array(t)))
                    else:
                        k3_=k3
                        X=numpy.array(json.loads(open(root+'X_'+k1+'_'+k2+'_'+k3_+'.txt', 'r').read()))

                    result[k1_][k2_][k3_]={}

                for s, k4 in enumerate(x_data_name_l4):
                    #k4='type'
                    result[k1_][k2_][k3_][k4]={}
                    stock_type=json.loads(open(root+x_type_path_list[0], 'r').read())
                    if isinstance(X, list):
                        a=numpy.array(stock_type).shape[0]
                        X=numpy.empty((a,0))
                    X=numpy.hstack((X,numpy.array(stock_type)))
                    #print 'x4, the shape is: ', X.shape

                    for p, k5 in enumerate(x_data_name_l5):
                        #k5='financial_index'
                        k5_=k5
                        if len(k5.strip())==0:
                            k5_='null'
                        else:
                            financial_index=json.loads(open(root+x_financial_path_list[0], 'r').read())
                            X=numpy.hstack((X,numpy.array(financial_index)))
                            #print 'financial index, the shape is: ', X.shape

                        result[k1_][k2_][k3_][k4][k5_]={}
                        #print k1_+'_'+k2_+'_'+k3_+'_'+k4+'_'+k5_
                        #print X.shape
                        #print '------------------------'
  
                        for q,y_k in enumerate(y_data_name):
                            y_k='Y_250'
                            q=6
                            result[k1_][k2_][k3_][k4][k5_][y_k]={}
                           
                            Y=numpy.array(json.loads(open(root+y_path_list[q], 'r').read()))
                            at=Y==0
                            z=Y[at]
                            print z.size
                            '''
                            #print 'the shape of X is: ', X.shape
                            #print 'the shape of Y is: ', Y.shape
                            dataset=split_dataset(X, Y,  stocks_years_flag)

                            
                            name=k1_+'_'+k2_+'_'+k3_+'_'+k4+'_'+k5_+'_'+y_k
                            #print '----------------------------------------'
                            #print name 
                           #print '-----------------------------'
                            #print 'the shape of X is: ', X.shape
                            #print 'the shape of Y is: ', Y.shape

                            model_result,result_print=model(dataset, name)
                            result[k1_][k2_][k3_][k4][k5_][y_k]=model_result
                            
                            for h, t in enumerate(type_flag_name):
                                print_result_data(result_print, type_name_dict, h, name+'_'+t, '')
                            print_result_data(result_print, type_name_dict, 0, name+'_year', 'year')
                            print_result_data(result_print, type_name_dict, 0, name+'_code', 'code')
                            '''

                            break
                        break
                    break
                break
            break
        break    
                            
    content=json.dumps(result)
    f=open('result/121521/ALL/all_model_result.txt', 'w')
    f.write(content)
    f.close()
               #break
    #break
    

if __name__=='__main__':
    main()
