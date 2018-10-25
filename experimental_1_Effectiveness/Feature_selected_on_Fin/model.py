# -*- coding: utf-8 -*-

from __future__ import division
import numpy as np
#import xgboost as xgb
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn import naive_bayes
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier

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
