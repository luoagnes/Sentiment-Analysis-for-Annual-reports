import numpy


def method1(senti_num, total_num):
    '''
    tone=1-N(pos/neg)/N(total)
    '''
    percent=senti_num/float(total_num)
    tone=1-percent
    return tone


def method2(pos_num, neg_num, total_num):
    '''
    tone=(pos_num-neg_num)/total_num
    '''

    tone=(pos_num-neg_num)/float(total_num)
    return tone


def method3(senti_num, total_num):
    '''
    the method is a central method and ready for later computation
    tone=(value-u)/std
    '''

    temp=senti_num/float(total_num)
    return temp

'''
def method4(senti_num_list, weight_list):
    score=0
    for i in range(len(senti_num_list)):
        score +=senti_num[i]*weight_list[i]
    return score
'''


def compute_delta_tone(tone_dict):
    
    result={}
    for stock in tone_dict.keys():
        result[stock] = {}
        for year in tone_dict[stock].keys():
            before_y=str(int(year)-1)
            if before_y not in tone_dict[stock].keys():
                continue
            result[stock][year]=tone_dict[stock][year]-tone_dict[stock][before_y]

    return result


def compute_std_tone(handle_dict):
    result={}
    for s in handle_dict.keys():
        temp=[]
        for y in handle_dict[s].keys():
            temp.append(handle_dict[s][y])

        d=numpy.array(temp)
        u=numpy.mean(d)
        std=numpy.std(d)
        result[s]={}
        for y in handle_dict[s].keys():
            key=s+'_'+y
            try:
                print handle_dict[s][y], u, std
                result[s][y]=(handle_dict[s][y]-u)/std
            except Exception:
                print 'u: ', u, ' std: ',std, ' value: ', handle_dict[s][y]
                return

    # final_result=compute_delta_tone(result)
    return result


def compute_tone_1(freq_dict, senti, total_name):
    result={}
    for key in freq_dict.keys():
        stock = key[:5]
        year = key[6:10]
        senti_num=freq_dict[key][senti]
        total_num=freq_dict[key][total_name]
        tone=method1(senti_num, total_num)

        if stock not in result.keys():
            result[stock]={}
        result[stock][year] = tone
    return result


def compute_tone_2(freq_dict, total_name):
    result={}
    for key in freq_dict.keys():
        stock = key[:5]
        year = key[6:10]

        pos_num=freq_dict[key]['pos']
        neg_num=freq_dict[key]['neg']
        total_num=freq_dict[key][total_name]
        tone=method2(pos_num, neg_num, total_num)

        if stock not in result.keys():
            result[stock]={}
        result[stock][year] = tone
    return result


def compute_tone_3(freq_dict, senti, total_name):
    first_tone_dict={}
    for key in freq_dict.keys():
        stock = key[:5]
        year = key[6:10]

        senti_num=freq_dict[key][senti]
        total_num=freq_dict[key][total_name]

        if stock not in first_tone_dict.keys():
            first_tone_dict[stock]={}
        first_tone_dict[stock][year]=method3(senti_num, total_num)

    result=compute_std_tone(first_tone_dict)
    return result





