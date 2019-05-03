import re
import time
import pandas as pd
from Spider import *

def LocateTable():
    html_file = open("../index.html", encoding='utf-8')
    html = "".join("".join(html_file.readlines()).split('\n'))
    
    html_parts = re.split("<table.*?.</table>", html)
    return html_parts

def ConvertToHtml(title, data_cols):
    d = {}
    index = 0
    for t in title:
        d[t]=data_cols[index]
        index = index+1
    df = pd.DataFrame(d)
    df = df[title]
    h = df.to_html(index=False)
    return h
def ADDLink(html, name_to_url):
    html_in_line = html.split('\n')
    print(html_in_line[11])
    print(html_in_line[17])
    print(html_in_line[23])
    print(html_in_line[11][10:-5])
    print(html_in_line[17][10:-5])
    print(html_in_line[23][10:-5])
    html_in_line[11] = "<td> <a href=\"%s\">%s</a> </td>"%(name_to_url[html_in_line[11][10:-5]], html_in_line[11][10:-5])
    html_in_line[17] = "<td> <a href=\"%s\">%s</a> </td>"%(name_to_url[html_in_line[17][10:-5]], html_in_line[17][10:-5])
    html_in_line[23] = "<td> <a href=\"%s\">%s</a> </td>"%(name_to_url[html_in_line[23][10:-5]], html_in_line[23][10:-5])
    html = "".join(html_in_line)
    return html

def ApplyCss(html):
    prefix = '<link rel="stylesheet" type="text/css", href="./CSS/df_style.css">'
    html = prefix+html
    regex = re.compile("<table.*")
    return regex.sub('<table border="1" class="dataframe mystyle">', html)

def Id2List(id_list):
    data_list = []
    for i in id_list:
        print(i)
        rootURL = 'https://cubingchina.com/results/person?region=World&gender=all&name='
        personList=[]
        num = int()
        
        resultHTML = getHTMLText (rootURL+i.split(',')[0])
        num = getPersonList (personList, resultHTML)  
        getPersonURL(personList)
        getPersonInfo(personList)

        data_list.append(personList[0][3])
    return data_list

event = '三阶'
mode = 0

def for_sort(item):
    if event in name_to_data[item]:
        if mode:
            if name_to_data[item][event][mode] != ' ':
                try:
                    return time.strptime(name_to_data[item][event][mode], "%S.%f")
                except:
                    return time.strptime(name_to_data[item][event][mode], "%M:%S.%f")
            else:
                return time.strptime('10.0', "%H.%f")
        else:
            try:
                return time.strptime(name_to_data[item][event][mode], "%S.%f")
            except:
                return time.strptime(name_to_data[item][event][mode], "%M:%S.%f")
    else:
        return time.strptime('10.0', "%H.%f")


if __name__ == '__main__':
    # data_cols = [['张三','李四','王二而'], [666, 666, 666], ['2016-08-25','2016-08-26','2016-08-27'], ['0769', '0976', '0999']]
    # title = ['姓名', '成绩', '日期', '详情']
    # html = ConvertToHtml(title, data_cols)
    # print(ConvertToHtml(title, data_cols))

    # name_to_url = {}
    # name_to_url['张三'] = 'https://www.baidu.com'
    # name_to_url['李四'] = 'https://www.github.com'
    # name_to_url['王二而'] = 'https://www.nwpu.edu.cn'
    # html = ADDLink(html, name_to_url)

    # # html = ApplyCss()
    # f = open("../yayaya.html", encoding='utf-8', mode='w')
    # f.write(html)

    f = open("wca_id.csv", encoding='utf-8')
    id_list = f.readlines()
    id_list = [i[:-1] for i in id_list]
    data_list = Id2List(id_list)
    # print(data_list)
    name_list = [i.split(',')[1] for i in id_list]

    name_to_data = dict(zip(name_list, data_list))
    # print(name_to_data)
    # print(name_to_data['Yuan Cao (操源)']['三阶'][1])
    events = ['三阶', '二阶', '四阶', '五阶', '六阶', '三盲', '最少步', '单手', '脚拧', '魔表', '五魔方', '金字塔', '斜转', 'SQ1', '四盲', '五盲', '多盲']
    modes = [0, 1]
    mode_str = ['单次', '平均']
    event_to_rank = {}
    for e in events:
        for m in modes:
            event = e
            mode  = m
            event_to_rank[e+mode_str[m]] = sorted(name_list, key=for_sort)[:3]
    html = ""
    for i in event_to_rank:
        title = ['姓名', '成绩', '日期', '详情']
        data_cols = []
        data_cols.append(event_to_rank[i])
        for i in range(3):
            t_list = ['']*3
            data_cols.append(t_list)
        html += "<hr>"
        html += ConvertToHtml(title, data_cols)
    # print(html)
    html = ApplyCss(html)
    f = open("../yayaya.html", encoding='utf-8', mode='w')
    f.write(html)

    # # print(event_to_rank)
    # for i in event_to_rank:
    #     for j in event_to_rank[i]:
            
    
    