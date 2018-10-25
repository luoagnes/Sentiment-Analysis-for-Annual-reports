#!-*- coding:utf8 -*-
import json
from financial_config import *
from Interface import *

ROE={
     '00004':{'2017':9.54},\
     '00010':{'2011':6.3},\
     '00020':{'2007':14.05},\
     '00101':{'2011':5.71},\
     '00439':{'2014':-21.76},\
     '00535':{'2005':10.6, '2013':30.2},\
     '00551':{'2012':12.22},\
     '00665':{'2008':6.07},\
     '00708':{'2009':19.25},\
     '01031':{'2011':5.17},\
     '02018':{'2017':33.55}
}

BV={'00665':{'2008':1845.5}, '01031':{'2011':13752.7}}

BPS={'00665':{'2008':1.49}, '01031':{'2011':1.13}}

EPS={
	'00101':{'2011':1.31},\
	'00136':{'2015':-0.01},\
        '00439':{'2014':-0.03},\
	'00467':{'2009':-0.03},\
	'00493':{'2004':0.05},\
	'00530':{'2010':0.04},\
	'00535':{'2005':0.03, '2013':0.15},\
	'00551':{'2012':2.07},\
	'00658':{'2008':0.15},\
	'00665':{'2003':0.05, '2008':0.1},\
	'00680':{'2003':0.002121},\
	'01031':{'2011':0.03},\
	'02007':{'2006':0.1},\
	'02314':{'2012':0.29},\
	'02689':{'2005':0.1},\
	'08279':{'2009':-0.05}
}


EM={
	'00530':{'2010':1.1132},\
	'00535':{'2005':2.503756,'2013':2.667378},\
	'00551':{'2012':1.707942},\
	'00665':{'2008':1.067464},\
	'00708':{'2009':1.350439},\
	'01031':{'2011':1.52532},\
	'02018':{'2017':1.750394}
}


def makeup(new_data, old_data, path):
    for s in new_data.keys():
        if s not in old_data.keys():
            old_data[s]={}

        for y in new_data[s].keys():
            old_data[s][y]=new_data[s][y]

    save_json(old_data, path)
    return old_data


def main():
    old_ROE_Diluted=json.loads(open(ROE_Diluted_dict_path,'r').read())
    old_ROE_Diluted=makeup(ROE, old_ROE_Diluted, ROE_Diluted_dict_path)
    normalized_data(old_ROE_Diluted, normalize_ROE_Diluted_dict_path)
    compute_delta_tone(old_ROE_Diluted, delta_ROE_Diluted_dict_path)

    old_BPS = json.loads(open(BPS_dict_path, 'r').read())
    old_BPS = makeup(BPS, old_BPS, BPS_dict_path)
    normalized_data(old_BPS, normalize_BPS_dict_path)
    compute_delta_tone(old_BPS, delta_BPS_dict_path)

    old_EPS = json.loads(open(EPS_dict_path, 'r').read())
    old_EPS = makeup(EPS, old_EPS, EPS_dict_path)
    normalized_data(old_EPS, normalize_EPS_dict_path)
    compute_delta_tone(old_EPS, delta_EPS_dict_path)


if __name__=='__main__':
    main()



    

