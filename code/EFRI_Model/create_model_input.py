# encoding: utf-8
'''
@author: yuyou
@file: create_Trajectory.py
@time: 2019/4/22 20:57
@desc: read
    @input:map_number.txt
    @ouput:T.txt/X.txt/W.txt
'''

import numpy as np
import os
import re
import time

#divided_map = np.loadtxt('map_number_900.txt' , dtype=np.int)
divided_map = np.loadtxt('map_number_840.txt' , dtype=np.int)
R = np.int(np.max(divided_map))+1

x_len = (104.21 - 103.93) / 3000
y_len = (30.79 - 30.56) / 2467

def outputT():#count a 48-dimension vector for each region(R=901).0-11 is inflow on workdays;12-23 is inflow on weekends;24-35 is outflow on workdays;36-47 is outflow on weekends.
    flow = np.zeros([R , 48])
    path_out = 'T_840.txt'
    for i in range(1, 31):
        if i < 10:
            path = r'G:\sourcedata\didi\txt\cc77888@qq.com_2016110' + str(i) + '\order_2016110' + str(i)
        else:
            path = r'G:\sourcedata\didi\txt\cc77888@qq.com_201611' + str(i) + '\order_201611' + str(i)
        print(path)
        with open(path, 'r') as f:
            for line in f.readlines():
                items = line.strip().split(',')
                t_o = int(items[1])
                timeArray = time.localtime(t_o)
                d = int(time.strftime("%d", timeArray))
                h = int(time.strftime("%H", timeArray))
                if d%7 == 5 or d%7 == 6: #weekend
                    t_o = 36 + int(h/2)
                else:
                    t_o = 24 + int(h/2)
                #print(t_o)
                t_d = int(items[2])
                timeArray = time.localtime(t_d)
                d = int(time.strftime("%d", timeArray))
                h = int(time.strftime("%H", timeArray))
                if d%7 == 5 or d%7 == 6:
                    t_d = 12 + int(h/2)
                else:
                    t_d = int(h/2)
                #print(t_d)

                lo_o = float(items[3])
                la_o = float(items[4])
                x = int((lo_o - 103.93)/x_len)
                y = int((30.79 - la_o)/y_len)
                if x >=0 and x < np.shape(divided_map)[1]:
                    if y >= 0 and y < np.shape(divided_map)[0]:
                        region_o = divided_map[y][x]
                        if region_o == 0:
                            try:
                                region_o = divided_map[y-1][x]
                                flow[region_o][t_o] += 0.2
                                region_o = divided_map[y][x-1]
                                flow[region_o][t_o] += 0.2
                                region_o = divided_map[y+1][x]
                                flow[region_o][t_o] += 0.2
                                region_o = divided_map[y][x+1]
                                flow[region_o][t_o] += 0.2
                                region_o = divided_map[y-1][x-1]
                                flow[region_o][t_o] += 0.05
                                region_o = divided_map[y-1][x+1]
                                flow[region_o][t_o] += 0.05
                                region_o = divided_map[y+1][x-1]
                                flow[region_o][t_o] += 0.05
                                region_o = divided_map[y+1][x+1]
                                flow[region_o][t_o] += 0.05
                            except:
                                x = 1
                        else:
                            flow[region_o][t_o] += 1
                lo_d = float(items[5])
                la_d = float(items[6])
                x = int((lo_d - 103.93)/x_len)
                y = int((30.79 - la_d)/y_len)
                if x >=0 and x < np.shape(divided_map)[1]:
                    if y >= 0 and y < np.shape(divided_map)[0]:
                        region_d = divided_map[y][x]
                        if region_d == 0:
                            try:
                                region_d = divided_map[y - 1][x]
                                flow[region_d][t_d] += 0.2
                                region_d = divided_map[y][x - 1]
                                flow[region_d][t_d] += 0.2
                                region_d = divided_map[y + 1][x]
                                flow[region_d][t_d] += 0.2
                                region_d = divided_map[y][x + 1]
                                flow[region_d][t_d] += 0.2
                                region_d = divided_map[y - 1][x - 1]
                                flow[region_d][t_d] += 0.05
                                region_d = divided_map[y - 1][x + 1]
                                flow[region_d][t_d] += 0.05
                                region_d = divided_map[x + 1][y - 1]
                                flow[region_d][t_d] += 0.05
                                region_d = divided_map[x + 1][y + 1]
                                flow[region_d][t_d] += 0.05
                            except:
                                region_d = 1
                        else:
                            flow[region_d][t_d] += 1
    for i in range(R):
        for j in range(12):
            flow[i][j] = flow[i][j]/22.0
        for j in range(12,24):
            flow[i][j] = flow[i][j]/8.0
        for j in range(24,36):
            flow[i][j] = flow[i][j]/22.0
        for j in range(36,48):
            flow[i][j] = flow[i][j]/8.0
    '''
    for j in range(48):
        total = 0
        for i in range(R):
            total += flow[i][j]
        for i in range(R):
            flow[i][j] = flow[i][j] / total
    '''
    np.savetxt(path_out , flow , fmt='%.8f' , delimiter='\t')

def outputX():#count a 18-dimension vector for each region(R=901).0-15 is number of various shops, and 16/17 stand for the number and price of houses, 18 is number of ganji shop.
    path_out = 'X_900.txt'
    type_vector = np.zeros([R , 19])
    respond = ['K歌','丽人','休闲娱乐','医疗健康','周边游','学习培训','宠物','宴会','榛果民宿','爱车','生活服务','电影演出赛事','结婚','美食','购物','运动健身']
    x_len = (104.21-103.93)/3000
    y_len = (30.79-30.56)/2467
    path_shop = r'G:\sourcedata\didi\shops_urls_la_lo.txt'
    path_xiaoqu = r'G:\sourcedata\didi\loupan_lalo.txt'
    path_ganji = r'G:\sourcedata\didi\ganji_company.txt'
    with open(path_shop , 'r' , encoding='utf-8') as f:
        for line in f.readlines():
            items = line.strip().split('\t')
            type = items[0]
            type = type.split(' ')
            type = respond.index(type[1])
            lalo = items[3]
            lalo = lalo.split(' ')
            lalo[0] = float(lalo[0])
            lalo[1] = float(lalo[1])
            x = int((lalo[0] - 103.93)/x_len)
            y = int((30.79 - lalo[1])/y_len)
            if x >=0 and x < np.shape(divided_map)[1]:
                if y >= 0 and y < np.shape(divided_map)[0]:
                    region = divided_map[y][x]
                    type_vector[region][type] += 1

    with open(path_xiaoqu , 'r' , encoding='utf-8') as f:
        for line in f.readlines():
            items = line.strip().split('\t')
            if len(items)>8:
                lo = float(items[8])
                la = float(items[7])
                x = int((lo - 103.93)/x_len)
                y = int((30.79 - la)/y_len)
                if x >=0 and x < np.shape(divided_map)[1]:
                    if y >= 0 and y < np.shape(divided_map)[0]:
                        region = divided_map[y][x]
                        single_price = re.findall( r'(\d+(\.\d+)?)' , items[3])
                        if single_price != []:
                            single_price = int(single_price[0][0])
                        else:
                            single_price = 0
                        if single_price < 2000:#每平米单价低于2000的划为一类（可能是未建成）
                            type_vector[region][16] += 1
                        else:
                            type_vector[region][17] += 1

    with open(path_ganji , 'r' , encoding='utf-8') as f:
        for line in f.readlines():
            items = line.strip().split('\t')
            if len(items)>1 and items[1][0] == '1':
                lalo = items[1].split()
                lo = float(lalo[0])
                la = float(lalo[1])
                print(lo , la)
                x = int((lo - 103.93)/x_len)
                y = int((30.79 - la)/y_len)
                print(x , y)
                if x >=0 and x < np.shape(divided_map)[1]:
                    if y >= 0 and y < np.shape(divided_map)[0]:
                        region = divided_map[y][x]
                        type_vector[region][18] += 1
    np.savetxt(path_out , type_vector , delimiter='\t' , fmt='%d')

    t = np.loadtxt(path_out , dtype=np.float)
    t2 = []
    for i in range(np.shape(t)[0]):
        for j in range(np.shape(t)[1]):
            if t[i][j] != 0:
                t2.append(t[i][j])
    t3 = np.array(t2)
    per_100 = []
    for i in range(0,100):#98 percentile divide 0-0.1237 into 99 intervals. beside an intervals with only zeros.
        per_100.append(np.percentile(t3,i))
    print(per_100)


    xx = {}
    for i in range(101):
        xx[i] = 0
    for i in range(np.shape(t)[0]):
        for j in range(np.shape(t)[1]):
            if t[i][j] == 0:
                t[i][j] = 0
                xx[0] += 1
            else:
                for k in range(len(per_100)):
                    if per_100[k]>t[i][j]:
                        t[i][j] = k
                        xx[k] += 1
                        break
                if t[i][j] < 1:
                    t[i][j] = 100
                    xx[100]+=1
    print(np.max(t))
    print(np.min(t))
    te = 0
    for key in xx.keys():
        print(key , xx[key])
        te += xx[key]
    np.savetxt(path_out , t , delimiter='\t' , fmt='%d')

def outputW():#count a Region*Review*Word matrix. Each number stand for the index of the word in candidate words,and may be count as an one-hot.
    #input:candidate words with index and frequency.
    #output:coordinate, content.(real type?)'---Region i---' as label of different region.followed by word index of words.

    #read all corpus, pick up shop name/review to index.
    path_out = 'W_840.txt'

    W_840 = [[] for i in range(R)]

    with open('fenci/region-index_dianping.txt' , 'r' ) as f1:
        for line in f1.readlines():
            item = line.strip().split('\t')
            if len(item) == 3:
                region = int(item[0])
                if region == 501:
                    if int(item[1]) != 10:
                        W_840[region].append(line)
                    else:
                        length = len(item[2].strip().split())
                        if length > 40:
                            W_840[region].append(line)
                else:
                    W_840[region].append(line)
            else:
                print(item)

    with open('fenci/region-index_fangtianxia.txt' , 'r') as f2:
        for line in f2.readlines():
            item = line.strip().split('\t')
            if len(item) == 3:
                region = int(item[0])
                W_840[region].append(line)
            else:
                print(item)

    with open('fenci/region-index_ganji.txt' , 'r') as f3:
        for line in f3.readlines():
            item = line.strip().split('\t')
            if len(item) == 3:
                region = int(item[0])
                W_840[region].append(line)
            else:
                print(item)

    with open(path_out , 'w') as f:
        for r in range(R):
            #f.write('---- Region ' + str(r) + ' ---\n')
            for m in range(len(W_840[r])):
                f.write(W_840[r][m])
            f.write('\n\n')
    '''
    '''
    max_review = 0
    max_word = 0
    for r in range(R):
        if len(W_840[r]) > max_review:
            max_review = len(W_840[r])
        for m in range(len(W_840[r])):
            item = W_840[r][m].split('\t')
            words = item[2].split()
            if len(words) > max_word:
                max_word = len(words)

    print('max review:',max_review)
    print('max words :',max_word)


def count_region():#pick up the regions with valid trajectory and shops.
    #pick up the index of empty region
    T_900 = np.loadtxt('T_900.txt')
    X_900 = np.loadtxt('X_900.txt' , dtype=np.int)
    T_empty = []
    X_empty = []
    for i in range(R):
        traj = np.sum(T_900[i])
        if traj < 0.00000001:
            T_empty.append(i)
    for i in range(R):
        traj = np.sum(X_900[i])
        if traj < 0.1:
            X_empty.append(i)
    print(len(T_empty))
    print(len(X_empty))
    clean = []
    for i in T_empty:
        if i in X_empty:
            clean.append(i)
    print(len(clean))

    #update T
    T_840 = np.delete(T_900 , clean , axis = 0)
    np.savetxt('T_840.txt' , T_840 , fmt='%8f' , delimiter='\t')

    #update X
    X_840 = np.delete(X_900 , clean , axis = 0)
    np.savetxt('X_840.txt' , X_840 , fmt='%d' , delimiter='\t')

    #update new map_number
    divided_map_840 = divided_map.copy()
    clean.sort(reverse=True)
    for i in clean:
        print(i)
        for x in range(np.shape(divided_map_840)[0]):
            for y in range(np.shape(divided_map_840)[1]):
                if divided_map_840[x][y] == i:
                    divided_map_840[x][y] = 0
                elif divided_map_840[x][y] > i:
                    divided_map_840[x][y] -= 1
    np.savetxt('map_number_840.txt' , divided_map_840 , fmt='%d' , delimiter='\t')
    print(np.max(divided_map_840))

def output_new_W():
    V = 17074
    Q = 6
    frequency = np.zeros([V , Q] , dtype=np.float)
    activity_type = {'0':0,'1':0,'2':0,'3':1,'4':2,'5':3,'6':0,'7':0,'8':0,'9':0,'10':0,'11':0,'12':0,'13':4,'14':4,'15':5}
    #activity_type = {'0':0,'1':0,'2':0,'3':1,'4':2,'5':3,'6':0,'9':0,'10':0,'11':0,'13':0,'14':0,'15':0,'16':4,'17':4,'18':5}
    with open('W_840.txt' , 'r') as f:
        for line in f.readlines():
            items = line.strip().split('\t')
            if len(items) == 3:
                typ = activity_type[items[1]]
                words = list(map(int , items[2].strip().split()))
                for i in words:
                    frequency[i-1][typ] += 1
    np.savetxt('activity_word_frequency_without_biaozhunhua.txt' , frequency , fmt='%d' ,delimiter='\t')
    frequency = frequency / np.sum(frequency, axis=0)[None , :]
    np.savetxt('activity_word_frequency.txt' , frequency , fmt='%.8f' ,delimiter='\t')

def output_190604_W():
    with open('W_840_old.txt' , 'r') as fin:
        with open('W_840.txt' , 'w') as fout:
            for line in fin.readlines():
                items = line.strip().split('\t')
                if len(items) > 2:
                    words = list(map(int , items[2].strip().split()))
                    for i in range(len(words)):
                        if words[i] >= 16468:
                            words[i] -= 1
                    words = list(map(str , words))
                    fout.write(items[0] + '\t' + items[1] + '\t' + ' '.join(words) + '\n')

    with open('fenci/candidate_words_with_fre.txt' , 'r' , encoding='utf-8') as fin:
        with open('candidate_words_with_fre.txt' , 'w' , encoding='utf-8') as fout:
            for line in fin.readlines():
                items = line.strip().split('\t')
                if len(items) == 3:
                    number = int(items[0])
                    if number > 16468:
                        fout.write(str(number-1) + '\t' +items[1] + '\t' + items[2] + '\n')
                    elif number < 16468:
                        fout.write(line)

    awfw = np.loadtxt('activity_word_frequency_without_biaozhunhua.txt' , dtype=np.int)
    awfw = awfw / np.sum(awfw , axis=0)[None , :]
    np.savetxt('activity_word_frequency.txt' , awfw , fmt='%.8f' , delimiter='\t')

if __name__ == '__main__':
    #count a 48-dimension vector for each region(R=901).
    outputT()

    #count a 21-dimension vector for each region(R=901)
    #outputX()

    #pick up the regions with valid trajectory and shops.Region number:900 decrease to 840
    #count_region()

    #count a Region*Review*Word matrix.
    #outputW()
    #output_new_W()
    #output_190604_W()

