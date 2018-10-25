#！-*- coding:utf8 -*-
import json
from config import *


def save_txt(content, path):
    f = open(path, 'w')
    if isinstance(content, unicode):
        content = content.encode('utf8')
    f.write(content)
    f.close()


def save_json(data, path):
    content=json.dumps(data, encoding='utf8', ensure_ascii=False)
    content=content.encode('utf8')
    save_txt(content, path)


def normalized_data(data):
    result = {}
    sum_result = {}
    for tone_kind in data['neg']['global'].keys():
        for s in data['neg']['global'][tone_kind].keys():
            for y in data['neg']['global'][tone_kind][s].keys():
                if tone_kind not in sum_result.keys():
                    sum_result[tone_kind] = []
                sum_result[tone_kind].append(round(data['neg']['global'][tone_kind][s][y],4))

    for tone_kind in data['neg']['global'].keys():
        min_v = min(sum_result[tone_kind])
        max_v = max(sum_result[tone_kind])
        for s in data['neg']['global'][tone_kind].keys():
            if s not in result.keys():
                result[s]={}
            for y in data['neg']['global'][tone_kind][s].keys():
                if y not in result[s].keys():
                    result[s][y]=[0,0,0]

                if max_v==min_v:
                    result[s][y]=1
                else:
                    result[s][y][int(tone_kind)-1] = round((data['neg']['global'][tone_kind][s][y] - min_v) / (max_v - min_v),4)

    return result


def main():
    result=[]
    # 1. read financial index
    financial_data=json.loads(open(fin_dict_path,'r').read())

    # 2. type data
    type_data=json.loads(open(type_code_dict_path, 'r').read())

    # 3. tone data
    tone_data=normalized_data(json.loads(open(delta_tone_dict_path, 'r').read()))

    # 4. label
    label_data=json.loads(open(gradient_dict_path, 'r').read())

    for stock in financial_data.keys():
        if stock not in type_data.keys():
            continue

        if stock not in tone_data.keys():
            continue

        if stock not in label_data.keys():
            continue

        for year in financial_data[stock].keys():
            if year not in tone_data[stock].keys():
                continue

            if year not in label_data[stock].keys():
                continue

            one_vector=type_data[stock]+[round(e, 4) for e in financial_data[stock][year]] +tone_data[stock][year]+[1 if label_data[stock][year]>0 else -1]
            result.append(one_vector)
    print len(result)
    save_json(result, experiment_1_dataset_path)


if __name__=='__main__':
    main()





