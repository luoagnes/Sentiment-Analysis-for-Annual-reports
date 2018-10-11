import os
import xlrd
import datetime
import pickle
from sklearn import linear_model
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

### %%% 1. get published date
font={'family':'serif', 'color':'darkred', 'weight':'normal', 'size':24}

def get_published_date(path):
    result={}

    wbk=xlrd.open_workbook(path)
    sheet=wbk.sheet_by_index(0)

    nrows=sheet.nrows

    for row in range(1,nrows):
        line=sheet.row_values(row)

        if line[0] not in result.keys():
            result[line[0]]={}

        result[line[0]][line[1]]=line[2]

    return result

### %%% 2.get price
def get_price(path):
    wbk=xlrd.open_workbook(path)
    sheet=wbk.sheet_by_index(0)

    date=sheet.col_values(0)[1:]
    close_price=sheet.col_values(4)[1:]

    date=[ d.strip().split(',')[0] for d in date]

    #print date[:10]
    #print close_price[:10]
    return date, close_price

### %%% 3. encode date
def encode_date(date_list):

    value_list=[]

    standard_date=datetime.datetime.strptime(date_list[0], '%Y-%m-%d')
    for date_str in date_list:
        current_date=datetime.datetime.strptime(date_str, '%Y-%m-%d')
        value=(current_date-standard_date).days
        value_list.append(value)
    return value_list

### %%% 4.regression and get a and b
def regression(X, Y):
    clf=linear_model.LinearRegression()
    clf.fit(X,Y)
    clf.predict(X)

    return clf.coef_[0][0], clf.predict(X)

def extract_one_year_data(standard_date, end_date, date, price):
    standard_date=datetime.datetime.strptime(standard_date, '%Y-%m-%d')
    end_date=datetime.datetime.strptime(end_date, '%Y-%m-%d')

    start_index=0
    end_index=0
    flag=False

    target_date=[]
    for d in date:
        current_date=datetime.datetime.strptime(d, '%Y-%m-%d')

        if not (current_date <standard_date):
            target_date.append(d)

            if not flag:
                start_index=date.index(d)
                flag=True

        if current_date >end_date:
            end_index=date.index(d)
            break
    target_price=price[start_index:end_index+1]
    encoded_date=encode_date(target_date)
    return target_date, encoded_date, target_price


### %%% 5. plot the line
def visularization(X, Y, Y_pre):
    plt.scatter(X, Y)
    plt.plot(X, Y_pre)
    plt.xlabel('close_price')
    plt.ylabel('date')
    plt.show()

def main():
    records=os.listdir('result/')

    ### get published date
    published_date=get_published_date('data/DOC_senti_words_true_l.xls')

    gradient={}
    root='data/price/'
    stock_files=os.listdir(root)
    for f in stock_files:   ## traverse each stock price file
        stock=f[:5]
        if stock not in published_date.keys():
            continue

        if stock not in gradient.keys():
            gradient[stock]={}

        file_path=root+f
        date, price=get_price(file_path)
        encoded_date=encode_date(date)

        ### start to regression and plot according to published_date
        #plt.figure(figsize=(64, 64))
        #plt.title(stock+'.HK')
        i=0

        for year in sorted(published_date[stock].keys()):
            i+=1
            if int(year)==2017:
                continue


            standard_date=published_date[stock][year]

            if str(int(year)+1) not in published_date[stock].keys():
                end_date=str(int(year)+1)+standard_date[4:]
            else:
               end_date=published_date[stock][str(int(year)+1)]
            target_date, encoded_date, target_price=extract_one_year_data(standard_date, end_date, date, price)


            X=np.array(zip(encoded_date))
            Y=np.array(zip(target_price))
            a, Y_pre=regression(X, Y)

            if a>0:
                gradient[stock][year]=1
            else:
                gradient[stock][year] = -1

            '''
            fig=plt.subplot(4,4,i)
            plt.scatter(X, Y)
            plt.plot(X, Y_pre)
            #plt.xlabel('close_date')
            #plt.ylabel('close_price')
            #plt.title(year+'-'+str(int(year)+1))

            ax=plt.gca()
            ax.set_xlabel('date', fontdict=font)
            ax.set_ylabel('close_price', fontdict=font)
            ax.set_xticklabels(('0','50', '100', '150', '200', '250', '300', '350', '400'))
            ax.set_title(year+'-'+str(int(year)+1),fontdict=font)
            '''
        #plt.show()
        #plt.savefig('result/'+stock+'.png')
        print stock, '------had finished !'
    output=open('gradient.pkl', 'wb')
    pickle.dump(gradient, output)
    output.close()

    return

if __name__=='__main__':
    main()


