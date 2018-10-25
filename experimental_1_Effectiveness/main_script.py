# -*- coding: utf-8 -*-
import numpy
import os
import pickle
from config2 import *
from sklearn.model_selection import KFold
from file_operation import *
from test_performance import get_performance_parameters
from model import * 
import json

def split_dataset(X, Y, stocks_years_flag):
    #print X.shape
    #print '----------split x is : ----------------'
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
    f=open(result_root+name+'_count_result.txt', 'w')
    f.write(content)
    f.close()
    return result
       
        
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
    if not os.path.exists(result_root):
        os.mkdir(result_root)
    
    stocks_years_flag=numpy.array(json.loads(open(root+years_flag_path, 'r').read()))
    type_name_dict=json.loads(open(type_flag_path, 'r').read())

    X=[]
    Y=[]
    for i, root_type in enumerate(X_root):
        result[root_type]={}
        for j, l1 in enumerate(X_l1):
            result[root_type][l1]={}
	    for h, l2 in enumerate(X_l2):
                result[root_type][l1][l2]={}
		for s, l3 in enumerate(X_l3):
                    l3_k=l3
                    if not isinstance(l3, list) and len(l3.strip()) > 0:
                        if root_type != 'ALL':
                            X_path = root + root_type + '/X_' + l1 + '_' + l2 + '_' + l3 + '.txt'
                            X = numpy.array(json.loads(open(X_path, 'r').read()))
                        else:
                            X1_path = root + '/MPE/X_' + l1 + '_' + l2 + '_' + l3 + '.txt'
                            X1 = json.loads(open(X1_path, 'r').read())
                            X2_path = root + '/OEE/X_' + l1 + '_' + l2 + '_' + l3 + '.txt'
                            X2 = json.loads(open(X2_path, 'r').read())
                            X = numpy.array(X1 + X2)
                        result[root_type][l1][l2][l3_k] = {}
                        # print X.shape, X_path


                    elif isinstance(l3, list):
                        X = numpy.array([])
                        l3_k = '_'.join(l3)
                        result[root_type][l1][l2][l3_k] = {}
                        for item in l3:
                            if root_type != 'ALL':
                                X_path = root + root_type + '/X_' + l1 + '_' + l2 + '_' + item + '.txt'
                                temp = json.loads(open(X_path, 'r').read())
                                print X.shape, numpy.array(
                                    temp).shape, X_path, '----l3 is list-----'
                                if X.shape[0] == 0:
                                    X = numpy.array(temp)
                                else:
                                    X = numpy.hstack((X, numpy.array(temp)))
                            else:

                                X1_path = root + '/MPE/X_' + l1 + '_' + l2 + '_' + item + '.txt'
                                X1 = json.loads(open(X1_path, 'r').read())
                                X2_path = root + '/OEE/X_' + l1 + '_' + l2 + '_' + item + '.txt'
                                X2 = json.loads(open(X2_path, 'r').read())

                                if X.shape[0] == 0:
                                    X = numpy.array(X1 + X2)
                                else:
                                    X = numpy.hstack((X, numpy.array(X1 + X2)))

                    else:
                        l3_k = 'null'
                        # l1='null'
                        # l2='null'
                        result[root_type][l1][l2][l3_k] = {}
                        X = []
                    print '------------------------------------------------------------------------'
		    for type_f in X_type:
                        type_k='null'
                        if len(type_f.strip())>0:
                            t=json.loads(open(root+root_type+'/'+type_f, 'r').read())
                            type_k=type_f
                            
                            #print root_type, l1, l2, l3, type_f, fin
                             
                            #print numpy.array(t).shape, X.shape, '----------add type-----------'
                            if isinstance(X, list):
                                num=len(t)
                                X=numpy.array([[] for i in range(num)])
                                X=numpy.hstack((X,numpy.array(t)))
                        result[root_type][l1][l2][l3_k][type_k]={}
			for fin in X_financial:
                            fin_k='null'
                            #if len(fin)==0:
                                #continue
                            #print root+root_type+'/'+fin
                            #F=numpy.array(json.loads(open(root+root_type+'/'+fin, 'r').read()))
                            #print F.shape, '--------------finnacial shape--------' 
				        
		            if len(fin.strip())>0:
                                fin_k=fin
                                financial=[]
                                if root_type !='ALL':
	                            financial=json.loads(open(root+root_type+'/X_financial_index.txt', 'r').read())
                                else:
                                   
                                    F1_path=root+'/MPE/X_financial_index.txt'
                                    F1=json.loads(open(F1_path, 'r').read())
                                    F2_path=root+'/OEE/X_financial_index.txt'
                                    F2=json.loads(open(F2_path, 'r').read())
                                    financial=F1+F2

                                #print numpy.array(financial).shape, X.shape, '-------------add financial--------'
                                
                                if isinstance(X, list):
    			            num=len(financial)
                                    X=numpy.array([[] for i in range(num)])
			        X=numpy.hstack((X,numpy.array(financial)))
                                                
                                         
			    result[root_type][l1][l2][l3_k][type_k][fin_k]={}
                            #print result
                            print '=================end ====================='
                            if isinstance(X, list):
    		                continue
			    for yi in Y_path_list:
                                Y_=[]
                                if root_type !='ALL':
				    Y_path=root+root_type+'/Y_'+yi+'.txt'
                                    Y_=json.loads(open(Y_path, 'r').read())
                                else:
                                                                    
                                    Y1_path=root+'/MPE/Y_'+yi+'.txt'
                                    Y1=json.loads(open(Y1_path, 'r').read())
                                    Y2_path=root+'/OEE/Y_'+yi+'.txt'
                                    Y2=json.loads(open(Y2_path, 'r').read())
                                    Y_=Y1+Y2

			        Y=numpy.array(Y_)
			        #print Y.shape, X.shape, '-----valide Y---------------'
				dataset=split_dataset(X, Y,  stocks_years_flag)
                                name= root_type+'_'+l1+'_'+ l2+'_'+l3_k+'_'+type_k+'_'+ fin_k+'_'+yi
				model_result,result_print=model(dataset, name)
                                #print fin_k, '-------^^^^^^^^^-----------'
				result[root_type][l1][l2][l3_k][type_k][fin_k][yi]=model_result
                                #print '---------^^^^^^^---------------------',model_result
                             
                                for h, t in enumerate(type_flag_name):
                                    print_result_data(result_print, type_name_dict, h, name+'_'+t, '')
    							
    content=json.dumps(result)
    f=open(result_root+'all_model_result.txt', 'w')
    f.write(content)
    f.close()
  
    
if __name__=='__main__':
    main()
