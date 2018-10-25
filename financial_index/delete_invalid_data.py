import json

delete_data={
'01113':[],
'00823':[],
'08008':[],
'87001':[],
'02778':[],
'00778':[],
'01076':[],
'00467':['2002','2003','2004','2005'],
'00336':['2002','2004'],
'01031':['2002','2003','2004'],
'00839':[],
'06060':[],
'01337':[],
'02232':[],
'02269':[],
'06088':[],
'00772':[],
'01458':[],
'01357':[]
}
del_year=['2009']

def del_data(data, path):
    result={}
    codes=delete_data.keys()
    for s in data.keys():
        
        if s in codes and len(delete_data[s])==0:
            continue
        result[s]={}
        for y in data[s].keys():
            if s in codes and y in delete_data[s]:
                continue
            if y in del_year:
                continue
            result[s][y]=data[s][y]

    content=json.dumps(result)
    f=open(path,'w')
    f.write(content)
    f.close()

if __name__=='__main__':
    ini_path='../result/financial_type_gradient.txt'
    data=json.loads(open(ini_path, 'r').read())
    del_data(data, ini_path)

            


