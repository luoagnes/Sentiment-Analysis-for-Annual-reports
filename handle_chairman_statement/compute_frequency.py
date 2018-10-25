#!-*- coding:utf8 -*-
"""
统计每一个年报中的negative， positive， total， global四个类别上的总词频数。
"""
import json
from config import Fre_count_dict_path, bow_word_vector_suffix, bow_word_vector_dict_path,doc_length_path


root_dict={'g':'global', 'p':'pos', 'n':'neg'}


def save_json(data, path):
    content=json.dumps(data)
    f=open(path, 'w')
    f.write(content)
    f.close()


def compute_freq():
    result={}
    total_num_dict=json.loads(open(doc_length_path, 'r').read())
    for k in root_dict.keys():
        path=bow_word_vector_dict_path+k+bow_word_vector_suffix
        senti_num_dict=json.loads(open(path, 'r').read())
        for key in senti_num_dict.keys():
            if key not in result.keys():
                result[key]={}

            result[key][root_dict[k]]=sum(senti_num_dict[key])

    for key in total_num_dict.keys():
        if key not in result.keys():
            result[key]={}

        result[key]['total']=total_num_dict[key]

    save_json(result, Fre_count_dict_path)


if __name__=='__main__':
    compute_freq()