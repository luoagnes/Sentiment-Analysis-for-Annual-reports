import xlwt
import json

def print_multi_dict(data_dict, path):
    wbk=xlwt.Workbook()
    sheet=wbk.add_sheet('sheet')

    col=0
    row=0

    for k1 in data_dict.keys():
        for k2 in data_dict[k1].keys():
            for k3 in data_dict[k1][k2].keys():
                for k4 in data_dict[k1][k2][k3].keys():
                    for k5 in data_dict[k1][k2][k3][k4].keys():
                        for k6 in data_dict[k1][k2][k3][k4][k5].keys():
                            for k7 in data_dict[k1][k2][k3][k4][k5][k6].keys():
                                data=data_dict[k1][k2][k3][k4][k5][k6][k7]
                                sheet.write(row, 0, k1)
                                sheet.write(row, 1, k2)
                                sheet.write(row, 2, k3)
                                sheet.write(row, 3, k4)
                                sheet.write(row, 4, k5)
                                sheet.write(row, 5, k6)
                                sheet.write(row, 6, k7)
                                col =7
                                for d in data:
                                    sheet.write(row, col, d)
                                    col +=1
                                row +=1

    wbk.save(path)


def print_multi_dict2(data_dict, path):
    wbk = xlwt.Workbook()
    sheet = wbk.add_sheet('sheet')

    col = 0
    row = 0
    title=["stock_list", "senti", "global_kind", "senti_tone", "type", "fin", "mmodel", "a","p","r","f1"]
    for til in title:
        sheet.write(row, col, til)
        col+=1

    row=1
    col=0
    for k1 in data_dict.keys():
        for k2 in data_dict[k1].keys():
            flag_list=k1.split('_')
            for flag in flag_list:
                sheet.write(row, col, flag)
                col+=1

            sheet.write(row, col, k2)

            col+=1
            data=data_dict[k1][k2]
            for d in data:
                sheet.write(row, col, d)
                col += 1
            row += 1
            col=0

    wbk.save(path)


if __name__=='__main__':
    data=json.loads(open('../result/all_model_result.txt', 'r').read())
    print_multi_dict2(data, '../result/all_model_result_norms_fin_tone.xls')
