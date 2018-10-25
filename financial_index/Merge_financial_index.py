# -*- coding: utf-8 -*-
from financial_config import *
from Interface import *

flag='delta_' # 'delta_'/''
save_flag='norm_delta_'


def merge_all_index():
    result={}
    result_clean={}
    financial_data_list=[]
    published_date=read_content(annual_report_published_date_path)

    for financial_index in financial_index_list: #norm_delta_ROE_Diluted_dict_path
        delta_index_path=eval(flag+financial_index+'_dict_path')
        content=normalized_data(read_content(delta_index_path), '')
        save_json(content, eval(save_flag+financial_index+'_dict_path'))
        financial_data_list.append(content)

    for s in published_date.keys():
        if s in financial_error_list:
            continue
        for y in published_date[s].keys():
            if s not in result.keys():
                result[s]={}
                result_clean[s]={}
            #result[s][y]=[]

            temp=[]
            for i, findex in enumerate(financial_data_list):
                if s in findex.keys() and y in findex[s].keys():
                    #result[s][y].append(findex[s][y])
                    temp.append(findex[s][y])
                else:
                    #result[s][y].append('NoN')
                    temp.append('NoN')

            if len(list(set(temp)))==1 and temp[0]=='NoN':
                continue

            if 'NoN' not in temp:
                result_clean[s][y]=temp
            result[s][y]=temp
    #normalized_data(result_clean, eval('count_' + flag + 'data_path') + '_norm_clean.txt')
    save_json(result, all_financial_index_pair_path+'_absence.txt')
    save_json(result_clean, all_financial_index_pair_path + '.txt')
    save_dict_to_excel(result, ['stock', 'year']+financial_index_list, all_financial_index_pair_path+'.xls')

    
if __name__=='__main__':
    merge_all_index()
    
                    
            
            
            
    


