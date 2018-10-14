import os
import json

root_pos='word_dict/Positive/'
root_neg='word_dict/Negative/'
root_global='word_dict/Global/'
root_list=[root_pos, root_neg, root_global]


def save_json(data, path):
    content=json.dumps(data)
    f=open(path, 'w')
    f.write(content)
    f.close()


def compute_freq():
    result={}
    for path in root_list:
        files=os.listdir(path)

        cate=path.split('/')[1]
    
        for f in files:
            k=f[:10]
            if k not in result.keys():
                result[k]={}
                result[k][cate]=0
        
            num=0
            w_dict=json.loads(open(path+f, 'r').read())
            for w in w_dict.keys():
                num +=w_dict[w]
            result[k][cate]=num
    
    total_num_path='result/docLength_all.txt'
    freq_dict=json.loads(open(total_num_path, 'r').read())
    for key in freq_dict.keys():
        result[key]['total']=freq_dict[key]
    save_json(result, 'result/freq_count.txt')


if __name__=='__main__':
    compute_freq()





            
        
