import xlwt
import json


root='data/delta_tone_dict.txt'

def read_json(path):
    content=json.loads(open(path, 'r').read())
    return content


def write_excel(data, path):
    wbk=xlwt.Workbook()

    for k in data.keys():
        sheet=wbk.add_sheet(k)
        content=data[k]
        col=0
        row=0
        for k1 in content.keys():
            for k2 in content[k1].keys():
                
                sheet.write(row, 0, k1)
                sheet.write(row, 1,k2)
                sheet.write(row, 2, content[k1][k2])
                row +=1
    wbk.save(path)


if __name__=='__main__':
    data=read_json(root)
    write_excel(data, 'result/delta_tone.xls')


