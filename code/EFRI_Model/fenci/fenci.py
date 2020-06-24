'''
@author: yuyou
@file: fenci.py
@time: 2019/4/26 14:41
@desc:
    @input:
    @output:
'''

import jieba
jieba.load_userdict("userdict.txt")
import jieba.analyse
import jieba.posseg as pseg
import numpy as np
import os
import re
import numpy as np
import datetime

path_all_word = 'all_single_words.txt'
path_candidate_word = 'final_candidate_words.txt'

stopwords = []
with open('stop_words.txt' , 'r' , encoding='utf-8') as f:
    for line in f.readlines():
        if line.strip() != '':
            stopwords.append(line.strip())

def sent2word(sentence):#Segment a sentence to words Delete stopwords
    segList = jieba.cut(sentence)
    segResult = []
    for w in segList:
        segResult.append(w.strip())

    newSent = []
    for word in segResult:
        if word not in stopwords and word != '':
            newSent.append(word)
    return newSent

def fenci_dianping():
    path_dianping = 'G:/sourcedata/didi/comment_sort'
    names = set()
    with open('words_dianping_comment.txt', 'w', encoding='utf-8') as fout:
        for file in os.listdir(path_dianping):
            if '结婚' not in file and '宴会' not in file and '民宿' not in file:
                whole_path = path_dianping + '/' + file
                print(whole_path)
                with open(whole_path , 'r' , encoding='utf-8') as fin:
                    for line in fin.readlines():
                        line = line.strip().split('\t')
                        if len(line) > 6:
                            names.add(line[0])
                            words = sent2word(line[6])
                            lin = ' '.join(words)
                            fout.write(line[0] + '\t' + lin + '\n')

    with open('words_dianping_shopname.txt', 'a', encoding='utf-8') as fout:
        for name in names:
            fout.write(name + '\n')

def fenci_weibo():
    with open(r'G:\sourcedata\didi\weibo_data.txt' , 'r' , encoding='utf-8') as fin:
        with open('words_weibo_without_coordinate.txt', 'w', encoding='utf-8') as fout:
            for line in fin.readlines():
                words = sent2word(line.strip())
                line = ' '.join(words)
                fout.write(line + '\n')

def fenci_news():
    with open(r'G:\sourcedata\didi\sinanews_data.txt' , 'r' , encoding='utf-8') as fin:
        with open('words_news_cont.txt', 'w', encoding='utf-8') as fout1:
            with open('words_news_title_without_coordinate.txt', 'w', encoding='utf-8') as fout2:
                for line in fin.readlines():
                    lin = line.strip().split('\t')
                    if len(lin)>2:
                        words = sent2word(lin[2].strip())
                        line = ' '.join(words)
                        fout1.write(line + '\n')
                        words = sent2word(lin[1].strip())
                        line = ' '.join(words)
                        fout2.write(line + '\n')

def fenci_fangtianxia():
    with open(r'G:\sourcedata\didi\comments_fangtianxia.txt' , 'r' , encoding='utf-8') as fin:
        with open('words_fangtianxia.txt', 'w', encoding='utf-8') as fout:
            for line in fin.readlines():
                line = line.strip().split('\t')
                words = sent2word(line[1].strip())
                words = ' '.join(words)
                fout.write(line[0] + '\t' + words + '\n')

def fenci_ganji():
    with open(r'G:\sourcedata\didi\company_content_all.txt' , 'r' , encoding='utf-8') as fin:
        with open('words_ganji.txt', 'w', encoding='utf-8') as fout:
            for line in fin.readlines():
                line = line.strip().split('\t')
                if len(line) > 3 and line[3] != '[收起]' and line[1] != '':
                    words = sent2word(line[3].strip())
                    words = ' '.join(words)
                    fout.write(line[1] + '\t' + words + '\n')


def fenci():
    print('weibo begin:')
    fenci_weibo()
    print('dianping begin:')
    fenci_dianping()
    print('news begin:')
    fenci_news()
    print('fangtianxia begin:')
    fenci_fangtianxia()
    print('ganji begin:')
    fenci_ganji()

def appear_dianping(word):
    with open('words_dianping_comment.txt' , 'r' , encoding='utf-8') as f:
        for line in f.readlines():
            if word in line:
                return 1
    return 0
def appear_ganji(word):
    with open('words_ganji.txt' , 'r' , encoding='utf-8') as f:
        for line in f.readlines():
            if word in line:
                return 1
    return 0
def appear_fangtianxia(word):
    with open('words_fangtianxia.txt' , 'r' , encoding='utf-8') as f:
        for line in f.readlines():
            if word in line:
                return 1
    return 0
def appear_news(word):
    with open('words_news_cont.txt' , 'r' , encoding='utf-8') as f:
        for line in f.readlines():
            if word in line:
                return 1
    return 0
def appear_weibo(word):
    with open('words_weibo_without_coordinate.txt' , 'r' , encoding='utf-8') as f:
        for line in f.readlines():
            if word in line:
                return 1
    return 0

def select_final():
    all_words = set()
    num_words = 0
    fre = {}
    corpus = []
    ori_file = ['words_dianping_comment.txt' , 'words_ganji.txt' , 'words_fangtianxia.txt']
    for file in ori_file:
        with open(file , 'r' , encoding='utf-8') as f:
            for line in f.readlines():
                item = line.strip().split('\t')
                if len(item) >1:
                    words = item[1].strip().split(' ')
                    for w in words:
                        all_words.add(w)
                        new_num = len(all_words)
                        if new_num > num_words:
                            fre[w] = 1
                            num_words = new_num
                        else:
                            fre[w] += 1

    fre_sorted = sorted(fre.items(), key=lambda x: x[1], reverse=True)

    with open('all_words.txt' , 'w' , encoding='utf-8') as f:
        for item in fre_sorted:
            if item[1] > 100:
                f.write(item[0] + '\t' + str(item[1]) + '\n')
    '''
    '''

    '''
    with open('all_words' , 'r' , encoding='utf-8') as f:
        with open('all_words.txt' , 'w' , encoding='utf-8') as fout:
            for line in f.readlines():
                item = line.strip().split()
                if u'\u4e00' <= item[0] <= u'\u9fff' or item[0][0].isalpha():
                    fout.write(line)

    appear = np.zeros(len(word))
    for key in word.keys():
        print(key)
        time_stamp = datetime.datetime.now()
        print("time_stamp:" + time_stamp.strftime('%Y.%m.%d-%H:%M:%S'))
        word[key] = appear_dianping(key) + appear_ganji(key) + appear_fangtianxia(key) + appear_weibo(key) + appear_news(key)
        if word[key] < 2:
            del word[key]
            print(key)
    with open('all_words2.txt' , 'w' , encoding='utf-8') as f:
        for key in word.keys():
            f.write(key + '\t' + fre[key] + '\n')
    '''


    fre = {}
    word_all_5 = {}
    with open('all_words.txt' , 'r' , encoding='utf-8') as f:
        for line in f.readlines():
            item = line.strip().split()
            fre[item[0]] = item[1]
    ori_file = ['words_dianping_comment.txt', 'words_ganji.txt', 'words_fangtianxia.txt']

    for name in fre.keys():
        word_all_5[name] = 0
    for file in ori_file:
        print(file)
        word_s = {}
        for name in fre.keys():
            word_s[name] = False
        with open(file , 'r' , encoding='utf-8') as f:
            for line in f.readlines():
                words = line.strip().split()
                for word in words:
                    word_s[word] = True
        for name in fre.keys():
            if word_s[name] == True:
                print(name)
                if file == 'words_dianping_comment.txt':
                    word_all_5[name] += 1
                else:
                    word_all_5[name] += 2
    with open('word_type_more_than_3.txt' , 'w' , encoding='utf-8') as f1:
        for name in fre.keys():
            if word_all_5[name] > 1:
                f1.write(name + '\t' + str(fre[name]) + '\n')


if __name__ == '__main__':
    #fenci()
    select_final()
    
    
    
    