# encoding: utf-8
'''
@author: yuyou
@file: word_explanation.py
@time: 2019/5/22 20:08
@desc:
'''

import numpy as np

if __name__ == "__main__":
    #folds = ['K=5,G=20' , 'K=8,G=20' , 'K=30,G=20' , 'K=10,G=5' , 'K=10,G=10' , 'K=10,G=20' , 'K=10,G=30']
    #for file in folds:
        #activity_embedding = np.loadtxt('result/'+file+'/rho_vi_mu.txt')
        activity_embedding = np.loadtxt('result/rho_vi_mu.txt')
        #print(activity_embedding)
        #word_embedding = np.loadtxt('result/'+file+'/eta_vi_mu.txt')
        word_embedding = np.loadtxt('result/xi_vi_mu.txt')
        word_embedding = word_embedding
        print(np.shape(activity_embedding))
        print(np.shape(word_embedding))
        Q = np.shape(activity_embedding)[0]
        G = np.shape(activity_embedding)[1]
        V = np.shape(word_embedding)[0]
        words = []
        with open('fenci/candidate_words_with_fre.txt' , 'r' , encoding='utf-8') as f:
            for line in f.readlines():
                words.append(line.strip().split()[1])

        for q in range(Q):
            Euc_distance = np.linalg.norm(activity_embedding[q] - word_embedding , axis=1)
            simi1 = Euc_distance.argsort()[-10:][::-1]
            word_simi1 = []
            for i in simi1:
                word_simi1.append(words[i])
            #print(word_simi1)
            Cos_distance = np.dot(activity_embedding[q] , word_embedding.T) / (np.linalg.norm(activity_embedding[q]) * np.linalg.norm(word_embedding , axis=1))
            simi2 = Cos_distance.argsort()[-20:][::-1]
            word_simi2 = []
            for i in simi2:
                word_simi2.append(words[i])
            print(word_simi2)


