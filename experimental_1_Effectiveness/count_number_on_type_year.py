import json
import xlwt


def save_dict_into_excel(data, path):
    wbk=xlwt.Workbook()
    sheet=wbk.add_sheet('sheet1')
    
    col=0
    row=0
    for a in data.keys():
        for i in data[a].keys():
            for y in data[a][i].keys():
                sheet.write(row, col, a)
                sheet.write(row, col+1, i)
                sheet.write(row, col+2, y)
                sheet.write(row, col+3, data[a][i][y])
                row +=1
    wbk.save(path)

    
def main(path):
    result={}
    type_name=json.loads(open('data/label_name.txt','r').read())
    stock_year=json.loads(open('result/stock_years_flag.txt','r').read())

    for item in stock_year:
        code=item[0]
        year=item[1]
        if code in type_name.keys():
            ab_type=type_name[code][0]
            ind_type=type_name[code][1]
            
            if ab_type not in result.keys():
                result[ab_type]={}
            if ind_type not in result[ab_type].keys():
                result[ab_type][ind_type]={}
            if year not in result[ab_type][ind_type].keys():
                result[ab_type][ind_type][year]=1
            else:
                result[ab_type][ind_type][year] +=1
    save_dict_into_excel(result, path)
    return result


if __name__=='__main__':
    path='result/count_on_ind_year.xls'
    main(path)
