# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 19:45:43 2017

@author: Administrator
"""

import json
from config import ini_WG_path, list_WG_path

def main(path, save_path):
    result=[]
    
    ### read txt
    f=open(path, 'rU')
    content=f.readlines()
    
    ### split and get word list
    for line in content[13:]:
        word_list=line.strip().split(',')[2:]
        word_str='-'.join(word_list)
        result.append(word_str)
        
    ### save word list into pkl
    #save_path='result/global_words.pkl'
    content=json.dumps(result)
    f=open(save_path, 'w')
    f.write(content)
    f.close()
    
    
    
if __name__=='__main__':
    path1=ini_WG_path+'global_words.txt'
    save_path1=list_WG_path+'global_words.txt'
    main(path1, save_path1)
    
    path1=ini_WG_path+'negative_words.txt'
    save_path1=list_WG_path+'Negative_list.txt'
    main(path1, save_path1)
    
    path1=ini_WG_path+'positive_words.txt'
    save_path1=list_WG_path+'Positive_list.txt'
    main(path1, save_path1)
    
    