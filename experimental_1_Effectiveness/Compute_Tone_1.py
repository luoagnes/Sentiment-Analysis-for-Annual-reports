
import json
from Tone_method import *
from config import ini_fre_dict_path, tone_dict_path, delta_tone_dict_path

senti_list=['pos', 'neg']
total_list=['global', 'total']


def save_json(data, path):
    content=json.dumps(data)
    f=open(path, 'w')
    f.write(content)
    f.close()

'''
def switch_dict_format(frequency_dict):
    result={}
    for k in frequency_dict.keys():
        for p in frequency_dict[k].keys():
            if p not in result.keys():
                result[p]={}
            result[p][k]=frequency_dict[k][p]
    return result
'''

def compute_ini_tone():
    tone_dict={}
    # 1. switch the format of frequency dict
    frequency_dict=json.loads(open(ini_fre_dict_path,'r').read())
    #freq_dict=switch_dict_format(frequency_dict)

    # 2. 
    for senti in senti_list:
        tone_dict[senti]={}
        for total in total_list:
            if total not in tone_dict[senti].keys():
                tone_dict[senti][total]={}
                tone_dict[senti][total]['1']=compute_tone_1(frequency_dict, senti, total)
                tone_dict[senti][total]['2'] = compute_tone_2(frequency_dict,  total)
                tone_dict[senti][total]['3'] = compute_tone_3(frequency_dict, senti, total)
    save_json(tone_dict, tone_dict_path)


def compute_l2_tone():
    result={}
    tone_dict=json.loads(open(tone_dict_path, 'r').read())
    
    for senti in tone_dict.keys():
        result[senti]={}
        for total_name in tone_dict[senti].keys():
            result[senti][total_name]={}
            result[senti][total_name]['1']=compute_delta_tone(tone_dict[senti][total_name]['1'])
            result[senti][total_name]['2']=compute_delta_tone(tone_dict[senti][total_name]['2'])
            result[senti][total_name]['3']=compute_delta_tone(tone_dict[senti][total_name]['3'])
            #result[l1_k]['4']=compute_delta_tone(tone_dict[l1_k]['4'])
    save_json(result, delta_tone_dict_path)


def main():
    compute_ini_tone()
    compute_l2_tone()


if __name__=='__main__':
    main()


            
             
    

