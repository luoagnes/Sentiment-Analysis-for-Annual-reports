# -*- coding: utf-8 -*-
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, fbeta_score, classification_report, \
    precision_recall_curve, roc_curve


def get_accuracy(y_true, y_pred):
    '''
    function: 获取该实验结果的accuracy
    y_true: 真实的类标
    y_pred：通过模型预测的类标

    '''
    accuracy = accuracy_score(y_true, y_pred, normalize=True, sample_weight=None)
    # print ('Accuracy Score (normalize=True):', accuracy)
    return accuracy


def get_precision(y_true, y_pred):
    '''
    function: 获取该实验结果的precision
    y_true: 真实的类标
    y_pred：通过模型预测的类标

    '''
    
    precision = precision_score(y_true, y_pred, average='macro')
    # print ('Precision Score:', precision)
    return precision


def get_recall(y_true, y_pred):
    '''
    function: 获取该实验结果的recall
    y_true: 真实的类标
    y_pred：通过模型预测的类标

    '''
    recall = recall_score(y_true, y_pred, average='macro')
    # print ('Recall Score :', recall)
    return recall


def get_F1(y_true, y_pred):
    '''
    function: 获取该实验结果的F1
    y_true: 真实的类标
    y_pred：通过模型预测的类标

    '''
    F1 = f1_score(y_true, y_pred, average='macro')
    # print ('F1 Score :', F1)
    return F1


def get_fbeta(y_true, y_pred):
    '''
    function: 获取该实验结果的fbeta
    y_true: 真实的类标
    y_pred：通过模型预测的类标

    '''
    fbeta = fbeta_score(y_true, y_pred, beta=0.001, average='macro')
    # print ('Fbeta Score :', fbeta)
    return fbeta


def get_classification_report(y_true, y_pred):
    '''
    function: 获取该实验结果的classification_report
    y_true: 真实的类标
    y_pred：通过模型预测的类标

    '''
    c_report = classification_report(y_true, y_pred, digits=2, target_names=['class_1', 'class_0', 'class_-1'])
    # print ( c_report)
    return c_report


def get_performance_parameters(y_true, y_pred):
    performance_parameters = {}
    a=get_accuracy(y_true, y_pred)
    p= get_precision(y_true, y_pred)
    r=get_recall(y_true, y_pred)
    f1=get_F1(y_true, y_pred)

    performance_parameters['accuracy'] = a
    performance_parameters['precision'] = p
    performance_parameters['recall'] = r
    performance_parameters['F1'] = f1
    return [a,p,r,f1]


if __name__ == '__main__':
    y_true = [1, 1, -1, -1, 0, -1, 0, 1]
    y_pred = [1, -1, -1, 0, 0, 1, 0, -1]
    get_performance_parameters(y_true, y_pred)
