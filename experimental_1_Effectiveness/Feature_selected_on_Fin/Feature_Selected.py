#!-*- coding:utf8 -*-
import numpy
import os
from sklearn.model_selection import KFold
from test_performance import get_performance_parameters
from model import *
import json

dataset_root_path='InputVec/'
result_root_path='result/'


def split_dataset(X, Y):
    # print X.shape
    # print '----------split x is : ----------------'
    X[X == '#'] = 0
    X[X == '-inf'] = 0
    X = X.astype(numpy.float64)
    Y[Y == 0] = 1
    if numpy.isnan(X).any():
        # X.dropna(inplace=True)
        X[numpy.isnan(X)] = 0
        # X[X==numpy.NAN]=0
    X = X  # [:,-21:]
    kf = KFold(n_splits=4)
    DataSet = []
    for train, test in kf.split(X):
        # DataSet.append([X[train],  X[test], Y[train],Y[test]])
        DataSet.append([X[train], X[test], Y[train], Y[test]])
    return DataSet


def one_model(dataset, path, method_name, method):
    method_train = []
    method_test = []

    print_result = {}
    train_print = []
    test_print = []

    for samples in dataset:
        #train_flag = samples[4]
        #test_flag = samples[5]
        samples = samples[:4]  # samples[:-2]
        # print samples[0].shape
        # print '-------------- above is the shape of input vector -------------'
        test_pred, train_pred = method(*samples)
        # print '---------- linear 2 is success ----------------'
        a = test_pred.shape[0]
        test_pred.shape = (a, 1)
        b = train_pred.shape[0]
        train_pred.shape = (b, 1)

        train = get_performance_parameters(samples[2], train_pred)
        test = get_performance_parameters(samples[3], test_pred)

        #temp_train = numpy.hstack((train_flag, samples[2], train_pred))
        #temp_test = numpy.hstack((test_flag, samples[3], test_pred))

        # print temp_train.shape
        # print temp_test.shape
        #train_print.append(temp_train.tolist())
        #test_print.append(temp_test.tolist())
        method_train.append(train)
        method_test.append(test)
        break
    # print len(train_print), len(train_print[0]), '\t', len(train_print[0][0]), '\t', type(train_print[0][0][0])
    # print numpy.array(train_print).shape
    print_result['train'] = numpy.array(train_print)
    print_result['test'] = numpy.array(test_print)
    # save_excel(path+'_'+method_name+'_train.xls', train_print)
    # save_excel(path+'_'+method_name+'_test.xls', test_print)

    LR_train = numpy.array(method_train).mean(axis=0)
    LR_test = numpy.array(method_test).mean(axis=0)

    return list(LR_train), list(LR_test), print_result


def model(dataset, path):
    result = {}
    result_print = {}

    train_result, test_result, print_result = one_model(dataset, path, 'LR', test_LogisticRegression)
    result['LR_train'] = train_result
    result['LR_test'] = test_result
    result_print['LR'] = print_result

    train_result, test_result, print_result = one_model(dataset, path, 'DT', test_DecisionTreeClassifier)
    result['DT_train'] = train_result
    result['DT_test'] = test_result
    result_print['DT'] = print_result

    train_result, test_result, print_result = one_model(dataset, path, 'RF', test_RandomForestClassifier)
    result['RF_train'] = train_result
    result['RF_test'] = test_result
    result_print['RF'] = print_result

    train_result, test_result, print_result = one_model(dataset, path, 'SVC_rbf', test_SVC_rbf)
    result['SVC_rbf_train'] = train_result
    result['SVC_rbf_test'] = test_result
    result_print['SVC_rbf'] = print_result

    train_result, test_result, print_result = one_model(dataset, path, 'SVC_linear', test_SVC_linear)
    result['SVC_linear_train'] = train_result
    result['SVC_linear_test'] = test_result
    result_print['SVC_linear'] = print_result

    # train_result, test_result=one_model(dataset, path, 'SVC_poly', test_SVC_poly)
    # result['SVC_polynorm_train'] =  train_result
    # result['SVC_polynorm_test'] =  test_result

    train_result, test_result, print_result = one_model(dataset, path, 'SVC_sig', test_SVC_sig)
    result['SVC_sigmoid_train'] = train_result
    result['SVC_sigmoid_test'] = test_result
    result_print['SVC_sigmoid'] = print_result

    #  -------------------test define kernel method ------------###
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
    # train_result, test_result=one_model(dataset, path, 'SVC_poly', test_SVC_poly)
    # result['SVC_polynorm_train'] =  train_result
    # result['SVC_polynorm_test'] =  test_result
    '''
    train_result, test_result, print_result=one_model(dataset, path, 'SVC_sig', test_SVC_sig2)
    result['SVC_sigmoid_train'] =  train_result
    result['SVC_sigmoid_test'] =  test_result
    result_print['SVC_sigmoid']=print_result
    '''
    # ----------------------------over-------------------------####
    train_result, test_result, print_result = one_model(dataset, path, 'GNB', test_GaussianNB)
    result['GNB_train'] = train_result
    result['GNB_test'] = test_result
    result_print['GNB'] = print_result

    '''
    train_result, test_result=one_model(dataset, path, 'MNB', test_MultinomialNB)
    result['MNB_train'] =  train_result
    result['MNB_test'] =  test_result
    '''

    train_result, test_result, print_result = one_model(dataset, path, 'BNB', test_BernoulliNB)
    result['BNB_train'] = train_result
    result['BNB_test'] = test_result
    result_print['BNB'] = print_result

    # print_final_result(result, 'result/121521/MPE/'+path+'_sum_result.xls')
    return result, result_print


def main():
    result={}
    data_kinds_list=os.listdir(dataset_root_path)
    for data_kind in data_kinds_list:
        if data_kind!='financial_index_dict':
            continue
        data_kind_path=dataset_root_path+data_kind+'/'
        stock_kinds_list=os.listdir(data_kind_path)

        if data_kind not in result.keys():
            result[data_kind]={}

        for stock_kind in stock_kinds_list:
            stock_kind_path=data_kind_path+stock_kind+'/inVec/'
            inputvec_list=os.listdir(stock_kind_path)

            if stock_kind not in result[data_kind].keys():
                result[data_kind][stock_kind]={}

            for filename in inputvec_list:
                data_path=stock_kind_path+filename
                label_path=data_kind_path+stock_kind+'/Label/'+filename

                X=numpy.array(json.loads(open(data_path, 'r').read()))
                Y=numpy.array(json.loads(open(label_path, 'r').read()))

                xname=filename.strip('.json')

                if X.shape[-1]==0 or Y.shape[-1]==0:
                    continue
                dataset = split_dataset(X, Y)
                model_result, result_print = model(dataset, xname)
                # print fin_k, '-------^^^^^^^^^-----------'
                result[data_kind][stock_kind][xname] = model_result
            print data_kind, '\t', stock_kind, '  ---over----'

    content = json.dumps(result)
    f = open( 'result/all_model_result_tone.txt', 'w')
    f.write(content)
    f.close()


if __name__ == '__main__':
    main()
