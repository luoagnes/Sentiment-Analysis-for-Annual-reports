import os
import xlwt
import json

root='result/121521/OEE/'


def write_dict(data, path):
    wbk=xlwt.Workbook()
    print 'start excel: ', path
    print len(data), '---------------------'
    for i,d in enumerate(data):
        print type(d), '  and ', len(d)
        sheet=wbk.add_sheet(d[1])
        print 'the %d sheet is: %s' % (i, d[1])
        row=0
        for m in d[0].keys():
            for t in d[0][m].keys():
                for k in d[0][m][t].keys():
                    if isinstance(d[0][m][t][k], dict):
                        for k2 in d[0][m][t][k].keys():
                            sheet.write(row, 0, m)
                            sheet.write(row, 1, t)
                            sheet.write(row, 2, k)
                            sheet.write(row, 3, k2)
                            sheet.write(row, 4, d[0][m][t][k][k2])
                            row +=1
                    else:
                        sheet.write(row, 0, m)
                        sheet.write(row, 1, t)
                        sheet.write(row, 2, k)
                        sheet.write(row, 3, d[0][m][t][k])
                        row +=1

    wbk.save(path)


target_files=[
'Negative_total_1_2_3_type_finanical_index_Y_250_year_count_result.txt',\
'Negative_total_1_2_3_type_finanical_index_Y_250_Industry_type_count_result.txt',\
'Negative_total_1_2_3_type_finanical_index_Y_250_code_count_result.txt',\
'Negative_total_1_2_3_type_finanical_index_Y_250_AB_type_count_result.txt'
]

def main():
    result=[]
    files=os.listdir(root)
    for f in files:
        #print '-----------------'
        #print '1111: ',f
        if not f.endswith('.txt'):
            continue
        #print '2222: ', f
        if f =='all_model_result.txt':
            continue
        #print '3333: ', f
        if 'Y_250' not in f:
            continue
        #print '4444: ', f
        if 'null' in f:
            continue
        #print '5555: ',f.split('type')[0].split('_')

        if len(f.split('type')[0].split('_'))>4:
            continue
        #print '6666: ', f

        d=json.loads(open(root+f, 'r').read())
        temp=f.split('_')
        path='_'.join([temp[0],temp[2]]+temp[8:-2])
        result.append([d,path])
        #print '=========================='
    #print 'handle data successful !!!'
    write_dict(result, root+'accuracy_count.xls')


if __name__=='__main__':
    main()
    
