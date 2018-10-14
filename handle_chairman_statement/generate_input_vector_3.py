# -*- coding: utf-8 -*-
import os
import numpy
import pickle
import csv
import json
from config import CS_word_dict_path, word_vector_root, one_hot_word_vector_dict_path, bow_word_vector_dict_path, bow_delta_tone_dict_path

root=CS_word_dict_path
P_senti_word_list=[]
N_senti_word_list=[]
G_senti_word_list=[]

stocks_list=[]

if not os.path.exists(word_vector_root):
    os.mkdir(word_vector_root)
	
if not os.path.exists(one_hot_word_vector_dict_path):
    os.mkdir(one_hot_word_vector_dict_path)
	
if not os.path.exists(bow_word_vector_dict_path):
    os.mkdir(bow_word_vector_dict_path)
	
if not os.path.exists(bow_delta_tone_dict_path):
    os.mkdir(bow_delta_tone_dict_path)
	

def read_files(path):
    files=[]
    
    for f in os.listdir(path):
        files.append(path+f)
    
    return files


def save_json_into_txt(data, path):
    content=json.dumps(data)
    f=open(path, 'w')
    if isinstance(data, unicode):
        content=content.encode('utf8')
    f.write(content)
    f.close()
    

def get_word_group_list():
    global N_senti_word_list
    global P_senti_word_list
    global G_senti_word_list

    n_file=os.listdir(root+'Negative/')[0]
    data_dict=json.loads(open(root+'Negative/'+n_file, 'r').read())
    N_senti_word_list=data_dict.keys()
    
    p_file=os.listdir(root+'Positive/')[0]
    data_dict=json.loads(open(root+'Positive/'+p_file, 'r').read())
    P_senti_word_list=data_dict.keys()
    
    g_file=os.listdir(root+'Global/')[0]
    data_dict=json.loads(open(root+'Global/'+g_file, 'r').read())
    G_senti_word_list=data_dict.keys()


def get_one_file_vector(file_path, senit_words_list):
    
    bow_vector=[]
    data_dict=json.loads(open(file_path, 'r').read())
   # print len(senit_words_list), '++++++++++++++++++++'
    for word_group in senit_words_list:
        #print data_dict[word_group]
        bow_vector.append(data_dict[word_group])
        
    one_hot_vector=list(map(lambda x: 1 if x>0 else 0, bow_vector))
    #print one_hot_vector, bow_vector
    return bow_vector, one_hot_vector


def get_all_vector(path, senti_words_list):
    bow_vector_dict={}
    one_hot_dict={}
    
    for f in os.listdir(path):
        key=f[:10].strip()
        file_path=path+f
        bow, one_hot=get_one_file_vector(file_path, senti_words_list)
        bow_vector_dict[key]=bow
        one_hot_dict[key]=one_hot
        
    return bow_vector_dict, one_hot_dict
   
    
def compute_delta_tone(vector_dict):
    result={}
    result_list=[]
    keys=vector_dict.keys()
    for key in keys:
        stock=key.split('_')[0]
        year=key.split('_')[1]
        
        if stock not in stocks_list:
            stocks_list.append(stock)
                
        before_key=stock+'_'+str(int(year)-1)
        if before_key in keys:
            delta_tone=list(map(lambda x, y: x-y, vector_dict[key], vector_dict[before_key]))
            result[key]=delta_tone
            #result_list.append(delat_tone)
    return result
            
 
def handle_vector(data_dict):
    result=[]
    for stock in stocks_list:
        for year in range(2001, 2018):
            key=stock+'_'+str(year)
            if key in data_dict:
                result.append(data_dict[key])
    return result


def write_one_sheet(data, title, table_obj, label):
    table_obj.writerow(['stocks', 'years', 'label', 'before_weighting_label']+title)

    for sy in data.keys():
        temp=sy.split('_')
        stock=temp[0].strip()
        year=temp[1].strip()

        if stock in label.keys() and year in label[stock].keys():
            instr_list=[stock, year, label[stock][year][0], label[stock][year][1]]+data[sy]
            table_obj.writerow(instr_list)


def print_data():
    mix_label = pickle.load(open('mix_label.pkl', 'r'))
    '''
    p_bow_delta_tone_dict=pickle.load(open('p_bow_delta_tone_dict.pkl', 'r'))
    f = open('p_bow_delta_tone.csv', 'w')
    writer = csv.writer(f)
    write_one_sheet(p_bow_delta_tone_dict, P_senti_word_list, writer, mix_label)
    f.close()

    n_bow_delta_tone_dict = pickle.load(open('n_bow_delta_tone_dict.pkl', 'r'))
    f = open('n_bow_delta_tone.csv', 'w')
    writer = csv.writer(f)
    write_one_sheet(n_bow_delta_tone_dict, N_senti_word_list, writer, mix_label)
    f.close()
    '''
    p_one_hot_dict = pickle.load(open('p_one_hot_dict.pkl', 'r'))
    f = open('p_one_hot.csv', 'w')
    writer = csv.writer(f)
    write_one_sheet(p_one_hot_dict, P_senti_word_list, writer, mix_label)
    f.close()

    n_one_hot_dict = pickle.load(open('n_one_hot_dict.pkl', 'r'))
    f = open('n_one_hot.csv', 'w')
    writer = csv.writer(f)
    write_one_sheet(n_one_hot_dict, N_senti_word_list, writer, mix_label)
    f.close()

    '''
    g_bow_delta_tone_dict = pickle.load(open('g_bow_delta_tone_dict.pkl', 'r'))
    f = open('g_bow_delta_tone.csv', 'w')
    writer = csv.writer(f)
    write_one_sheet(g_bow_delta_tone_dict, G_senti_word_list, writer, mix_label)
    f.close()

    g_one_hot_dict = pickle.load(open('g_one_hot_dict.pkl', 'r'))
    f = open('g_one_hot.csv', 'w')
    writer = csv.writer(f)
    write_one_sheet(g_one_hot_dict, G_senti_word_list, writer, mix_label)
    f.close()
    '''


def main():
    
    p_path=root+'Positive/'
    #print len(P_senti_word_list), len(N_senti_word_list)
    p_bow_vector_dict, p_one_hot_dict=get_all_vector(p_path, P_senti_word_list)
    save_json_into_txt(p_bow_vector_dict, bow_word_vector_dict_path+'p_bow_vector_dict.txt')
    save_json_into_txt(p_one_hot_dict, one_hot_word_vector_dict_path+'p_onehot_dict.txt')
    p_bow_delta_tone_dict=compute_delta_tone(p_bow_vector_dict)
    #p_one_hot_dict=compute_delta_tone(p_one_hot_dict)
    #p_one_hot_array=numpy.array(handle_vector(p_one_hot_dict))
    #p_bow_delta_tone_array=numpy.array(handle_vector(p_bow_delta_tone_dict))
    save_json_into_txt(p_bow_delta_tone_dict, bow_delta_tone_dict_path+'p_bow_delta_tone_dict.txt')
    #pickle.dump(p_one_hot_dict, open('p_one_hot_dict.pkl', 'w'))

    
    
    n_path=root+'Negative/'
    n_bow_vector_dict, n_one_hot_dict=get_all_vector(n_path, N_senti_word_list)
    save_json_into_txt(n_bow_vector_dict, bow_word_vector_dict_path+'n_bow_vector_dict.txt')
    save_json_into_txt(n_one_hot_dict, one_hot_word_vector_dict_path+'n_onehot_dict.txt')
    n_bow_delta_tone_dict=compute_delta_tone(n_bow_vector_dict)
    #n_one_hot_dict=compute_delta_tone(n_one_hot_dict)
    #n_one_hot_array=numpy.array(handle_vector(p_one_hot_dict))
    #n_bow_delta_tone_array=numpy.array(handle_vector(p_bow_delta_tone_dict))
    save_json_into_txt(n_bow_delta_tone_dict, bow_delta_tone_dict_path+'n_bow_delta_tone_dict.txt')
    #pickle.dump(n_one_hot_dict, open('n_one_hot_dict.pkl', 'w'))
    
    g_path=root+'Global/'
    g_bow_vector_dict, g_one_hot_dict=get_all_vector(g_path, G_senti_word_list)
    save_json_into_txt(g_bow_vector_dict, bow_word_vector_dict_path+'g_bow_vector_dict.txt')
    save_json_into_txt(g_one_hot_dict, one_hot_word_vector_dict_path+'g_onehot_dict.txt')
    #g_one_hot_array = numpy.array(handle_vector(g_one_hot_dict))
    g_bow_delta_tone_dict=compute_delta_tone(g_bow_vector_dict)
    g_bow_delta_tone_array = numpy.array(handle_vector(g_bow_vector_dict))
    pickle.dump(g_bow_vector_dict, open('g_bow_tone_dict.pkl', 'w'))
    save_json_into_txt(g_bow_delta_tone_dict, bow_delta_tone_dict_path+'g_bow_delta_tone_dict.txt')
    #pickle.dump(g_one_hot_dict, open('g_one_hot_dict.pkl', 'w'))

    '''
    g_bow_delta_tone_dict=compute_delta_tone(g_bow_vector_dict)
    g_one_hot_dict=compute_delta_tone(g_one_hot_dict)
    g_one_hot_array=numpy.array(handle_vector(g_one_hot_dict))
    g_bow_delta_tone_array=numpy.array(handle_vector(g_bow_delta_tone_dict))
    pickle.dump(g_bow_delta_tone_dict, open('g_bow_delta_tone_dict.pkl', 'w'))
    pickle.dump(g_one_hot_dict, open('g_one_hot_dict.pkl', 'w'))
    '''
    

if __name__=='__main__':
    get_word_group_list()
    #main()
    print len(G_senti_word_list)
    print len(P_senti_word_list)
    print len(N_senti_word_list)
    main()
    
    
    

