'''
@author: yuyou
@file: lalo-to-region.py
@time: 2019/4/26 19:20
@desc:
    @input:
    @output:
'''
import numpy as np


divided_map = np.loadtxt('../map_number_840.txt' , dtype=np.int)
x_len = (104.21 - 103.93) / 3000
y_len = (30.79 - 30.56) / 2467

#x = int((lo_o - 103.93) / x_len)   y = int((30.79 - la_o) / y_len)

'''
'''
candidate_words = {}
with open('candidate_words_with_fre.txt' , 'r' , encoding='utf-8') as f:
    for line in f.readlines():
        item = line.strip().split()
        candidate_words[item[1]] = int(item[0])
def dianping_lalo():
    coor = {}
    respond = ['K歌', '丽人', '休闲娱乐', '医疗健康', '周边游', '学习培训', '宠物', '爱车', '生活服务', '电影演出赛事', '美食', '购物', '运动健身']
    shop_type = {}
    with open('G:\sourcedata\didi\shops_urls_la_lo.txt' , 'r' , encoding='utf-8') as f:
        for line in f.readlines():
            items = line.strip().split('\t')
            lalo = items[3]
            lalo = lalo.split(' ')
            lalo[0] = float(lalo[0])
            lalo[1] = float(lalo[1])
            x = int((lalo[0] - 103.93) / x_len)
            y = int((30.79 - lalo[1]) / y_len)
            if x >= 0 and x < np.shape(divided_map)[1]:
                if y >= 0 and y < np.shape(divided_map)[0]:
                    region = divided_map[y][x]
                    coor[items[2]] = region
            temp = items[0].split(' ')
            shop_type[items[2]] = respond.index(temp[1])


    with open('words_dianping_comment.txt' , 'r' , encoding='utf-8') as f:
        with open('region-index_dianping.txt' , 'w') as fout:
            for line in f.readlines():
                items= line.strip().split('\t')
                if len(items) > 1:
                    if items[0] in coor.keys():
                        string = str(coor[items[0]]) + '\t' + str(shop_type[items[0]]) + '\t'
                        sent = items[1].split(' ')
                        c=0
                        for se in sent:
                            if se in candidate_words.keys():
                                c+= 1
                                string += ' ' + str(candidate_words[se])
                        if c > 0:
                            fout.write(string + '\n')


def fangtianxia():
    coor = {}
    with open('G:\sourcedata\didi\loupan_lalo.txt' , 'r' , encoding='utf-8') as f:
        for line in f.readlines():
            items = line.strip().split('\t')
            if len(items) > 8:
                lo = float(items[8])
                la = float(items[7])
                x = int((lo - 103.93) / x_len)
                y = int((30.79 - la) / y_len)
                if x >= 0 and x < np.shape(divided_map)[1]:
                    if y >= 0 and y < np.shape(divided_map)[0]:
                        region = divided_map[y][x]
                        coor[items[0]] = region
                        
    with open('words_fangtianxia.txt' , 'r' , encoding='utf-8') as f:
        with open('region-index_fangtianxia.txt' , 'w') as fout:
            for line in f.readlines():
                items= line.strip().split('\t')
                if len(items) > 1:
                    if items[0] in coor.keys():
                        string = str(coor[items[0]]) + '\t14\t'
                        sent = items[1].split(' ')
                        c=0
                        for se in sent:
                            if se in candidate_words.keys():
                                c+= 1
                                string += ' ' + str(candidate_words[se])
                        if c > 0:
                            fout.write(string + '\n')

def ganji():
    with open('words_ganji.txt', 'r', encoding='utf-8') as f:
        with open('region-index_ganji.txt' , 'w') as fout:
            for line in f.readlines():
                item = line.strip().split('\t')
                #region
                if len(item) > 1:
                    string = ''
                    lalo = item[0].split(' ')
                    x = int((float(lalo[0]) - 103.93) / x_len)
                    y = int((30.79 - float(lalo[1])) / y_len)
                    if x >=0 and x < np.shape(divided_map)[1]:
                        if y >= 0 and y < np.shape(divided_map)[0]:
                            region = divided_map[y][x]
                            string = str(region) + '\t15\t'
                    #index
                    sent = item[1].split()
                    c=0
                    for se in sent:
                        if se in candidate_words.keys():
                            c+= 1
                            string += ' ' + str(candidate_words[se])
                    if c > 0:
                        fout.write(string + '\n')

def ganji_count():
    number = set()
    with open('words_ganji.txt', 'r', encoding='utf-8') as f:
            for line in f.readlines():
                item = line.strip().split('\t')
                #region
                if len(item) > 1:
                    number.add(item[0])
    print(len(number))


def create_candidate_words():
    with open('word_type_more_than_3.txt' , 'r' , encoding='utf-8') as fin:
        with open('candidate_words_with_fre.txt', 'w', encoding='utf-8') as fout:
            data = fin.readlines()
            for i in range(len(data)):
                fout.write(str(i+1) + '\t' + data[i])

if __name__ == '__main__':
    '''
    create_candidate_words()
    ganji()
    fangtianxia()
    dianping_lalo()
    '''
    ganji_count()
    
    
    