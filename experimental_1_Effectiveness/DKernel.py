#-*-  coding: UTF-8 -*-
import numpy as np
import numpy.linalg as LA

q=0.01


def linear(X,Y):
    '''
    线性核
    :param X:
    :param Y:
    :return:
    '''
    kernel_train=np.dot(X, np.transpose(Y))
    return kernel_train


def Polynomial(X,Y):
    '''
    多项式核
    '''
    b=0.1
    c=0.1
    p=2
    kernel_train = np.power((b*(np.dot(X, np.transpose(Y))+c)),p)
    return kernel_train


def Gaussian(X,Y):
    '''
    高斯核
    '''
    m=X.shape[0]
    print 'X shape is: ', X.shape
    print 'Y shape is: ', Y.shape
    kernel_matrix=np.zeros((m,m))
    
    for i in range(m):
        for j in range(m):
            kernel_matrix[i,j] = np.exp(np.power(LA.norm(X[i]-Y[j], 2),2)*(-10))
    print 'kernel train shape is: ', kernel_matrix.shape
    return kernel_train


def Exponential(X,Y):
    '''
     指数核，高斯核的变种
    '''

    kernel_train = np.exp(LA.norm(X - Y, 2) * (-1 / (2 * q*q)))
    return kernel_train


def Laplacian(X,Y):
    '''
    拉普拉斯核，完全等价于指数核，但对参数更敏感，也是一种径向基核函数
    '''
    kernel_train = np.exp(LA.norm(X - Y, 2) * (-1 /q))
    return kernel_train


def ANOVA(X,Y):
    '''
    ANOVA 核，径向基核函数一族，其适用于多维回归问题
    '''
    k=2
    d=2
    t=np.power(np.power(X,k)-np.power(Y, k),2)
    kernel_train = np.power(np.exp(t * (-1*q)), d)
    return kernel_train



def Sigmoid(X,Y):
    '''
    sigmoid 核
    '''
    a=0.1
    c=0.1
    kernel_train = np.tanh(a*np.dot(X,np.transpose(Y))+c)
    return kernel_train


def Rational_Quadratic(X,Y):
    '''
    二次有理核，可以作为高斯核的替代品，但是没有高斯核那么耗时，但是同时对参数也十分敏感
    '''
    c=0.1
    t=np.power(LA.norm(X-Y,2),2)
    kernel_train = 1-t/(t+c)
    return kernel_train


def Multiquadric(X,Y):
    '''
    多元二次核，可以代替二次有理核，是一种非正定核函数。
    '''
    c=0.1
    kernel_train = np.power((np.power(LA.norm(X-Y,2),2)+c*c), 0.5)
    return kernel_train


def Inverse_Multiquadric(X,Y):
    '''
    逆多元二次核，据说该核函数不会遇到矩阵奇异的情况
    '''
    c=0.1
    kernel_train = np.power((np.power(LA.norm(X - Y, 2), 2) + c * c), -0.5)
    return kernel_train


def Circular(X, Y):

    t=LA.norm(X-Y,2)
    a=2/np.pi * np.arccos(-1/q * t)
    b=2/np.pi * (t/q)*np.power((1-t*t/q),0.5)
    kernel_train = a-b
    return kernel_train


def Spherical(X,Y):
    '''
    Circular核函数的简化版
    '''
    t=LA.norm(X-Y,2)
    kernel_train = 1-3/2*t/q + 1/2*np.power(np.power(t,2)/q,3)
    return kernel_train


def Wave(X, Y):
    '''
    据说适用于语音场景
    '''
    c=0.1
    t=LA.norm(X-Y,2)
    kernel_train = c/t*np.sin(t/c)
    return kernel_train


def Triangular(X, Y):
    '''
    三角核函数，是多元二次核的特例
    '''
    d=2
    kernel_train = -1*np.power(LA.norm(X-Y,2),d)
    return kernel_train


def Log(X, Y):
    d=2
    kernel_train = -1 * np.log(1+np.power(LA.norm(X-Y,2),d))
    return kernel_train


def Cauchy(X, Y):
    '''
    柯西核函数
    '''
    t=np.power(LA.norm(X-Y,2),2)
    kernel_train = 1/(t/q+1)
    return kernel_train


def Chi_Square(X,Y):
    '''
    卡方核
    '''
    kernel_train = 1-np.sum(2*np.power(X-Y,2)/(X+Y))
    return kernel_train


def Generalized_T_S(X, Y):
    '''

    :return:
    '''
    d=2
    kernel_train = 1/(1+np.power(LA.norm(X-Y,2),d))
    return kernel_train






