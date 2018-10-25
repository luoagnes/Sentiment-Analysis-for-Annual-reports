# -*- coding: utf-8 -*-

from __future__ import division
import numpy as np
#import xgboost as xgb
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn import naive_bayes
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from DKernel import *

### logistic regression classifier##############################
def test_LogisticRegression(*data):
    X_train, X_test, y_train, y_test = data
    cls = LogisticRegression(penalty ='l2',C=3)
    cls.fit(X_train, y_train)
    cls.predict(X_test)
    return cls.predict(X_test), cls.predict(X_train)
### test following paramters:
# C=np.logspace(-2, 4, num=100)
###


### decision tree classifier##############################
def test_DecisionTreeClassifier(*data):
    X_train, X_test, y_train, y_test = data

    cls = DecisionTreeClassifier(max_depth =50)
    cls.fit(X_train, y_train)
    return cls.predict(X_test), cls.predict(X_train)

    ###
    '''
   criterions=['gini', 'entropy']
   splitter=['best', 'random']
   max_depth=np.arrange(1, maxdepth)
   '''
    ###

### ----------Bayes -----#######
### --------- naive Bayes--------

def test_GaussianNB(*data):
    X_train, X_test, y_train, y_test = data

    cls = naive_bayes.GaussianNB()
    cls.fit(X_train, y_train)
    return cls.predict(X_test), cls.predict(X_train)

def test_MultinomialNB(*data):
    X_train, X_test, y_train, y_test = data

    cls = naive_bayes.MultinomialNB()
    cls.fit(X_train, y_train)
    return cls.predict(X_test), cls.predict(X_train)

def test_BernoulliNB(*data):
    X_train, X_test, y_train, y_test = data
    #print 'X_train is ----------------'
    #print X_train
    #print '----------------'

    #print 'X_test is---------------------'
    #print X_test
    #print '--------------------------'

    #print 'y_train is--------------------'
    #print y_train
    #print '-------------------------------'
    #print 'y_test is ------------------'
    #print y_test

    cls = naive_bayes.BernoulliNB()
    cls.fit(X_train, y_train)
    return cls.predict(X_test), cls.predict(X_train)

  
#### svm classifier##############################
def test_SVC_rbf(*data):
    X_train, X_test, y_train, y_test = data
    cls = svm.SVC(kernel='rbf', gamma=10, C=5)
    cls.fit(X_train, y_train)
    return cls.predict(X_test), cls.predict(X_train)

def test_SVC_linear(*data):
    X_train, X_test, y_train, y_test = data
    cls = svm.LinearSVC()
    cls.fit(X_train, y_train)
    return cls.predict(X_test), cls.predict(X_train)

def test_SVC_poly(*data):
    X_train, X_test, y_train, y_test = data
    cls = svm.SVC(kernel='poly', gamma=10, C=5)
    cls.fit(X_train, y_train)
    return cls.predict(X_test), cls.predict(X_train)

def test_SVC_sig(*data):
    X_train, X_test, y_train, y_test = data
    cls = svm.SVC(kernel='sigmoid', gamma=10, C=5)
    cls.fit(X_train, y_train)
    return cls.predict(X_test), cls.predict(X_train)

### defined by myself ---###
def test_SVC_rbf2(*data):
    X_train, X_test, y_train, y_test = data
    cls = svm.SVC(kernel=Gaussian)
    #kernel_X=Gaussian(X_train,X_train)
    #kernel_test=Gaussian(X_test,X_test)
    #print 'kernel train is: ', kernel_X.shape, ' X train is: ', X_train.shape, ' y train is: ', y_train.shape
    
    cls.fit(X_train, y_train)
    return cls.predict(X_test), cls.predict(X_train)

def test_SVC_linear2(*data):
    X_train, X_test, y_train, y_test = data
    cls = svm.SVC(kernel='precomputed')
    kernel_X=linear(X_train,X_train)
    kernel_test=linear(X_test, X_train)
    print 'liner kernel: ',kernel_X.shape, ' the ini X shape is: ', X_train.shape
    print 'Y_train shape is: ', y_train.shape
    cls.fit(kernel_X, y_train)
    return cls.predict(kernel_test), cls.predict(kernel_X)


def test_SVC_sig2(*data):
    X_train, X_test, y_train, y_test = data
    cls = svm.SVC(kernel='precomputed')
    kernel_X=Sigmoid(X_train,X_train)
    cls.fit(kernel_X, y_train)
    return cls.predict(X_test), cls.predict(X_train)



### test paramters: gamma  for svm.SVC
'''
gamma=range(1, 20)
'''
###

def test_SVR_rbf(*data):
    X_train, X_test, y_train, y_test = data
    cls = svm.SVR(kernel='rbf', gamma=10)
    cls.fit(X_train, y_train)
    return cls.predict(X_test), cls.predict(X_train)


###
'''test following paramters:
gamma=range(1,20)
'''
###

##########random forest classifier##############################
def test_RandomForestClassifier(*data):
    X_train, X_test, y_train, y_test = data
    cls = RandomForestClassifier(n_estimators=11, max_depth=10)
    cls.fit(X_train, y_train)
    return cls.predict(X_test), cls.predict(X_train)

'''
############# gcforest classifier##############################
def test_GcForest(*data):
    X_train, X_test, y_train, y_test = data
    gcf = gcForest()
    gcf.fit(X_train, y_train)
    return gcf.predict(X_test)


def test_XGBoost(*data):
    X_train, X_test, y_train, y_test = data
    xg_train = xgb.DMatrix(X_train, label=y_train)
    xg_test = xgb.DMatrix(X_test, label=y_test)

    ### setup parameters for xgboost
    param = {}

    ## use softmax multi-class classification
    param['objective'] = 'multi:softmax'

    ### scale weight of positive example
    param['eta'] = 0.1
    param['max_depth'] = 6
    param['silent'] = 1
    param['nthread'] = 4
    param['num_class'] = 6

    watchlist = [(xg_train, 'train'), (xg_test, 'test')]
    num_round = 5
    bst = xgb.train(param, xg_train, num_round, watchlist)

    # get prediction
    pred = bst.predict(xg_test)
    error_rate = np.sum(pred != y_test) / y_test.shape[0]
    print ('Test error using softmax = {}'.format(error_rate))

    ### do the same thing again, but output probabilities
    param['objective'] = 'multi:softprob'
    bst = xgb.train(param, xg_train, num_round, watchlist)

    ### get prediction, this is in ID array, need reshape to (ndata, nclass)
    pred_prob = bst.predict(xg_test).reshape(y_test.shape[0], 6)
    pred_label = np.argmax(pred_prob, axis=1)
    error_rate = np.sum(pred != y_test) / y_test.shape[0]
    print ('Test error using softprob = {}'.format(error_rate))
    return pred
'''
