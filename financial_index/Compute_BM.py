# -*- coding: utf-8 -*-
'''
BM=BookValue/marketCapitalization
'''
from financial_config import *
from Interface import *


def compute_BM(market_capitalization, Book_value, path):
    BM_dict={}
    for s in market_capitalization.keys():
        BM_dict[s]={}
        for y in market_capitalization[s].keys():
            if s in Book_value.keys() and y in Book_value[s].keys():
                a=market_capitalization[s][y]
                b=Book_value[s][y]
                print 'a: ', a, type(a), '----'
                print 'b: ', b, type(b), '----'
                print '---------------'
                if not isinstance(a, float) and '-' not in str(a):
                     a=float(a)
                if not isinstance(b, float) and '-' not in str(b):
                    b=float(b)

                if isinstance(a, float) and isinstance(b, float):
                    temp='#'
                    if a==0:
                        temp='#'
                    else:
                        temp=b/a
                    if s=='01668' and y=='2009':
                        print s, '\t', y, '\t', a, '\t', b, '\t',temp
                    BM_dict[s][y]=temp
    save_json(BM_dict, path)
    return BM_dict
    

def Handle_BM_data():
    # 1. read_data
    market_capitalization = json.loads(open(Market_capitalization_dict_path, 'r').read())
    Book_value = json.loads(open(Book_Value_dict_path, 'r').read())

    # 2. compute
    BM_dict=compute_BM(market_capitalization, Book_value, BM_dict_path)

    # 5. normalized the market capitalization
    normalized_data(BM_dict, normalize_BM_dict_path)

    # 6. compute delta market capitalization
    compute_delta_tone(BM_dict, delta_BM_dict_path)


if __name__=='__main__':
    Handle_BM_data()
    print '--------------------Done----------------'
    

