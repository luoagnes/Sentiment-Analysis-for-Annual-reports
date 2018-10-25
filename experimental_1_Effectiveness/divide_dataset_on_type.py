import json
import os
import numpy as np

def save_json(data, path):
    content=json.dumps(data)
    f=open(path, 'w')
    f.write(content)
    f.close()


def divide_index():
    OEE=[]
    MPE=[]
    type_list=json.loads(open('result/X_type.txt', 'r').read())
    
    for i, item in enumerate(type_list):
        if item[0]==1:
            OEE.append(i)
        else:
            MPE.append(i)
    print 'OEE is: ', len(OEE), 'MPE is: ', len(MPE)
    return OEE, MPE


def split_data(OEE, MPE):
    files=os.listdir('result/')
    for f in files:
        if not f.endswith('.txt'):
            continue
        data=json.loads(open('result/'+f, 'r').read())
        temp1=np.array(data)[OEE].tolist()
        save_json(temp1, 'result/OEE/'+f)

        temp2=np.array(data)[MPE].tolist()
        save_json(temp2, 'result/MPE/'+f)


def main():
    OEE, MPE=divide_index()
    split_data(OEE, MPE)

if __name__=='__main__':
    main()
        
        


        
    

    
            
    
