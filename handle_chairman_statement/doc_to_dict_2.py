# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 20:05:43 2017

@author: Administrator
"""
import json
import os
from nltk.book import FreqDist
from nltk.corpus import PlaintextCorpusReader
from config import filtered_CS_path, CS_word_dict_path,doc_length_path,interim_path, list_WG_path,ini_WG_path

Not_list=[]
Negative_list=[]
Positive_list=[]
global_words_list=[]

def save_json(data, path):
    content=json.dumps(data)
    f=open(path, 'w')
    f.write(content)
    f.close()
    
    
def get_dict():
    Negative_list=json.loads(open(list_WG_path+'Negative_list.txt','r').read())
    Positive_list=json.loads(open(list_WG_path+'Positive_list.txt','r').read())
    global_words_list=json.loads(open(list_WG_path+'global_words.txt','r').read())
    
    Not_list=[s.strip() for s in open(ini_WG_path+'Not.txt', 'rU').readlines()]
    return Negative_list, Positive_list, Not_list, global_words_list
    
def load_corpus(corpus_root):
    corpus_reader=PlaintextCorpusReader(corpus_root, '.*')
    file_list=corpus_reader.fileids()
    return corpus_reader, file_list

def isNot_Arround(word_list, w):
    index=word_list.index(w)
    Judgment_range=word_list[index-5:index]
    
    for word in Judgment_range:
        if word.upper() in Not_list:
            return True
    return False

def isInDict(SentiList, w):
    for s in SentiList:
        temp_list=s.strip().split('-')
        if w.lower() in temp_list:
            return s
    return None
    
def save_docLlength(corpus_reader, file_list):
    length_dict={}
    
    for f in file_list:
        key=f[0:10]
        word=corpus_reader.words(fileids=f)
        length=len(word)
        
        if length <5:
            continue
        length_dict[key]=length
    save_json(length_dict, doc_length_path)
    
           
    
def doc2sentiment_dict(fname, corpus_reader, SentiList, save_name):
    result={}
	
    n=save_name.count('/')
    dirname_list=save_name.split('/')[:-1]
    for i in range(n):
        dirpath='/'.join(dirname_list[:i+1])+'/'
        if not os.path.exists(dirpath):
		    os.mkdir(dirpath)
    
    word_list=list(set(corpus_reader.words(fileids=fname)))
    print 'the length of words are: ', len(word_list)
    print 'the set length is: ', len(list(set(word_list)))
    fdist=FreqDist(word_list)
    
    if len(word_list)==0:
        f=open(interim_path+'empty_file.txt', 'a+')
        f.write(fname+'\n')
        f.close()
        print (fname,'-----------')
        return
    
    for w in word_list:
        
        key_str=isInDict(SentiList, w)
        if key_str !=None and (not isNot_Arround(word_list, w)):
            if key_str not in result.keys():
                result[key_str]=0
            result[key_str] +=fdist[w]
    
    for str in SentiList:
        if str not in result.keys():
            result[str]=0
    save_json(result, save_name)
    
    return result

def main(corpus_reader,file_list, start, end):
    for f in file_list[start:end]:
        path=CS_word_dict_path+'Negative/'+f[0:10]+'_Negative.txt'
        if os.path.exists(path):
            print 'path is not exists!',path
            continue
        doc2sentiment_dict(f, corpus_reader, Negative_list, CS_word_dict_path+'Negative/'+f[0:10]+'_Negative.txt')
			
        doc2sentiment_dict(f, corpus_reader, Positive_list, CS_word_dict_path+'Positive/'+f[0:10]+'_Positive.txt')
			
        doc2sentiment_dict(f, corpus_reader, global_words_list, CS_word_dict_path+'Global/'+f[0:10]+'_global_words.txt')
        
if __name__=='__main__':
    corpus_root=filtered_CS_path
    corpus_reader, file_list=load_corpus(corpus_root)
    save_docLlength(corpus_reader, file_list)
    Negative_list, Positive_list, Not_list, global_words_list=get_dict()
    
    length=len(file_list)
    print '--------------------'
    main(corpus_reader,file_list,0, length)
    print '---------end---------'
    
   
    
    
