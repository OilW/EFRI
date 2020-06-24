# -*- coding: utf-8 -*-
# Time:2018/12/27 20:45
# Author: yuyou

import datetime
import math
import numpy as np
import scipy.special
import os

os.environ["CUBA_VISIBLE_DEVICES"] = "1"

'''
需要文件：
人流量           T.txt   R*N，离散成R*N*I
文本输入         W.txt   R*M*D
商店类别输入      X.txt   R*F
简化需要中间文件：
所有候选词with index and frequency       candidate words.txt         V*3
'''
Threshold = 0.01
ITER = 1000
Learning_rate = 0.0001
R = 841  # number of regions
K = 5  # number of topics
V = 17073  # number of candidate words
Q = 6  # number of activities
# M=1000
M = 57628  # max number of reviews in a region
N = 48  # number of 24 time bins with inflow and outflow
I = 1221  # to discretize trajectory flow,we divide it into I interval
F = 16  # number of shop types
# D=100
D = 839  # max number of words in a single review
G = 20  # embedding dimension of words and activities

word_fres = np.loadtxt('activity_word_frequency.txt')

def get_W():
    M_r = np.zeros(R, dtype=np.int)
    D_rm = np.zeros([R, M], dtype=np.int)
    W = [[] for r in range(R)]
    W_Q = [[] for r in range(R)]
    word_belong_activity = np.argmax(word_fres , axis=1)

    with open('W_840.txt', 'r') as f:
        for line in f.readlines():
            items = line.strip().split('\t')
            if len(items) == 3:
                region = int(items[0])
                words = items[2].strip().split(' ')
                belong_Q = []
                length = len(words)
                if length < 2:
                    for d in range(length):
                        QQ = []
                        words[d] = int(words[d])-1
                        QQ.append(word_belong_activity[words[d]])
                        belong_Q.append(QQ)
                elif length < 6:
                    for d in range(length):
                        words[d] = int(words[d])-1
                    for d in range(length):
                        QQ = []
                        x = words.copy()
                        x.remove(words[d])
                        for item in x:
                            QQ.append(word_belong_activity[item])
                        belong_Q.append(QQ)
                else:
                    for d in range(length):
                        words[d] = int(words[d])-1
                    for d in range(length):
                        QQ = []
                        if d == 0:
                            QQ = [word_belong_activity[words[1]] , word_belong_activity[words[2]] , word_belong_activity[words[3]] , word_belong_activity[words[4]]]
                        elif d == 1:
                            QQ = [word_belong_activity[words[0]] , word_belong_activity[words[2]] , word_belong_activity[words[3]] , word_belong_activity[words[4]]]
                        elif d == length-1:
                            QQ = [word_belong_activity[words[d-4]] , word_belong_activity[words[d-3]] , word_belong_activity[words[d-2]] , word_belong_activity[words[d-1]]]
                        elif d == length-2:
                            QQ = [word_belong_activity[words[d-3]] , word_belong_activity[words[d-2]] , word_belong_activity[words[d-1]] , word_belong_activity[words[d+1]]]
                        else:
                            QQ = [word_belong_activity[words[d-2]] , word_belong_activity[words[d-1]] , word_belong_activity[words[d+1]] , word_belong_activity[words[d+2]]]
                        belong_Q.append(QQ)

                W[region].append(words)
                W_Q[region].append(belong_Q)
                D_rm[region][M_r[region]] = length
                M_r[region] += 1
    M_mean = np.mean(M_r)
    D_mean = np.mean(D_rm)
    return [W , W_Q , M_r , D_rm , M_mean , D_mean]

print(datetime.datetime.now(), 'init begin!')

[W , W_Q , M_r , D_rm , M_mean , D_mean] = get_W()

# init parameter
b = np.random.rand(G)
sigma_lambda = np.random.randint(1, 5, size=F)
sigma_c = np.random.randint(1, 5, size=Q)  # Q*1
sigma_psi = np.random.randint(1, 5, size=G)
sigma_w = np.random.randint(1 , 5)  # a scalar
beta = np.random.randint(1, 5, size=I)
epsilon = np.random.randint(1, 5, size=Q)

# create variational parameter
phi_vi = np.random.randint(1, 5, size=(K, I))
# phi_vi = phi_vi / np.sum(phi_vi, axis=1)[:, None]

pi_vi = np.random.randint(1, 5, size=(K, Q))
pi_vi_sigma = (pi_vi + 1) / (np.sum(pi_vi , axis=1)[: , None] +1)
pi_vi = (pi_vi) / (np.sum(pi_vi , axis=1)[: , None])
pi_vi_sigma = pi_vi_sigma * pi_vi

xi_vi_mu = np.random.rand(Q, G)
xi_vi_sigma = np.zeros([Q, G])
# xi_vi_mu = xi_vi_mu / np.sum(xi_vi_mu, axis=1)[:, None]

psi_vi_mu = np.random.rand(V , G)
psi_vi_sigma = np.zeros([V , G])
# psi_vi_mu = psi_vi_mu / np.sum(psi_vi_mu, axis=1)[:, None]

lambda_vi_mu = np.random.rand(K, F)
lambda_vi_sigma = np.ones([K, F])
lambda_vi_mu = lambda_vi_mu / np.sum(lambda_vi_mu, axis=1)[:, None]

alpha_vi = np.random.rand(R, K)
# alpha_vi = alpha_vi / np.sum(alpha_vi, axis=1)[:,:, None]

theta_vi = np.random.rand(R, K)
theta_vi = theta_vi / np.sum(theta_vi, axis=1)[:, None]

y_vi = np.random.rand(R, M, K)
y_vi = y_vi / np.sum(y_vi, axis=2)[:, :, None]

z_vi = np.random.rand(R, N, K)
z_vi = z_vi / np.sum(z_vi, axis=2)[:, :, None]

# read observed data
X = np.loadtxt('X.txt', dtype=np.float)

T = np.loadtxt('T_840.txt', dtype=np.int)

print(datetime.datetime.now(), 'W init complete!')


def Estep(count):
    global phi_vi
    phi_vi_old = phi_vi.copy()
    global pi_vi
    global pi_vi_sigma
    pi_vi_old = pi_vi.copy()
    pi_vi_sigma_old = pi_vi_sigma.copy()
    global xi_vi_mu
    global xi_vi_sigma
    xi_vi_mu_old = xi_vi_mu.copy()
    xi_vi_sigma_old = xi_vi_sigma.copy()
    global psi_vi_mu
    global psi_vi_sigma
    psi_vi_mu_old = psi_vi_mu.copy()
    psi_vi_sigma_old = psi_vi_sigma.copy()
    global lambda_vi_mu
    global lambda_vi_sigma
    lambda_vi_mu_old = lambda_vi_mu.copy()
    lambda_vi_sigma_old = lambda_vi_sigma.copy()
    global alpha_vi
    alpha_vi_old = alpha_vi.copy()
    global theta_vi
    theta_vi_old = theta_vi.copy()
    global y_vi
    y_vi_old = y_vi.copy()
    global z_vi
    z_vi_old = z_vi.copy()

    # some useful expression
    Digamma_phi_vi_K_I_subtract_sum = scipy.special.digamma(phi_vi_old)-scipy.special.digamma(np.sum(phi_vi_old, axis=1))[: , None]
    #Digamma_pi_vi_K_Q_subtract_sum = scipy.special.digamma(pi_vi_old)-scipy.special.digamma(np.sum(pi_vi_old, axis=1))
    Digamma_theta_vi_R_K_subtract_sum = scipy.special.digamma(theta_vi_old)-scipy.special.digamma(np.sum(theta_vi_old , axis = 1))[: , None]
    xi_vi = xi_vi_mu * xi_vi_mu + 2 * xi_vi_sigma
    psi_vi = psi_vi_mu * psi_vi_mu + psi_vi_sigma

    # update phi_vi
    print(datetime.datetime.now(), 'update phi_vi begin:')
    phi_vi = np.ones([K , I]) * beta
    for r in range(R):
        for n in range(N):
            i = T[r][n]
            for k in range(K):
                    phi_vi[k][i] += z_vi_old[r][n][k]
    # phi_vi = phi_vi / np.sum(phi_vi, axis=1)[:, None]
    phi_vi_nan = np.isnan(phi_vi).sum()
    if phi_vi_nan > 0:
        print(phi_vi)
        print('nan appear phi')
    phi_vi_rmse = np.sqrt(np.average((phi_vi - phi_vi_old) ** 2))


    # update pi_vi,xi_vi,psi_vi,y_vi
    print(datetime.datetime.now(), 'update pi_vi,xi_vi,psi_vi,y_vi begin:')
    pi_vi = np.ones([K, Q]) * epsilon
    fenzi_xi = np.ones([Q, G]) * (sigma_w / b)
    fenmu_xi = np.dot(np.sum(np.dot(y_vi_old , pi_vi_sigma_old) , axis=(0 , 1)).reshape(-1 , 1) , np.sum(psi_vi , axis=0).reshape(1 , -1))
    fenzi_psi = np.zeros([V , G])
    fenmu_psi = np.ones([V , G]) * (np.sum(np.dot(np.dot(y_vi_old , pi_vi_sigma_old) , xi_vi) , axis=(0,1)) + sigma_w/sigma_psi)
    y_vi_exps = np.ones([R , M , K]) * Digamma_theta_vi_R_K_subtract_sum[: , None , :]
    for r in range(R):
        for m in range(M_r[r]):
            for d in range(D_rm[r][m]):
                v = W[r][m][d]
                belong_Q = W_Q[r][m][d]
                #pi
                for q in belong_Q:
                    pi_vi[: , q] += y_vi_old[r][m] * np.dot(xi_vi_mu_old[q] , psi_vi_mu_old[v])

                #xi
                for q in belong_Q:
                    fenzi_xi[q] += np.dot(y_vi_old[r][m] , pi_vi_old[: , q]) * psi_vi_mu[v]

                #psi
                fenzi_psi[v] += np.sum(np.dot(y_vi_old[r][m].reshape(1 , -1) , np.dot(pi_vi_sigma_old[: , belong_Q] , xi_vi_mu_old[belong_Q])) , axis=(0,1))

                #y
                temp = 2 * np.dot(pi_vi_old[: , belong_Q] , np.dot(xi_vi_mu_old[belong_Q] , psi_vi_mu_old[v])) + np.dot(pi_vi_sigma_old[: , belong_Q] , np.dot(xi_vi[belong_Q] , psi_vi[v])) + 1
                y_vi_exps[r][m] += temp / 2 / sigma_w


    pi_vi_sigma = (pi_vi + 1) / (np.sum(pi_vi, axis=1)[:, None] + 1)
    pi_vi = (pi_vi) / (np.sum(pi_vi, axis=1)[:, None])
    pi_vi_sigma = pi_vi_sigma * pi_vi
    pi_vi_rmse = np.sqrt(np.average((pi_vi - pi_vi_old) ** 2))
    pi_vi_nan = np.isnan(pi_vi).sum()
    if pi_vi_nan > 0:
        print(pi_vi)
        print('nan appear pi' , pi_vi_nan)

    xi_vi_mu = fenzi_xi / fenmu_xi
    xi_vi_mu = xi_vi_mu / np.sum(xi_vi_mu , axis=1)[: , None]
    xi_vi_sigma = sigma_w / fenmu_xi
    xi_vi_mu_rmse = np.sqrt(np.average((xi_vi_mu - xi_vi_mu_old) ** 2))
    xi_vi_sigma_rmse = np.sqrt(np.average((xi_vi_sigma - xi_vi_sigma_old) ** 2))
    xi_vi_nan = np.isnan(xi_vi_mu).sum()
    if xi_vi_nan > 0:
        print(xi_vi)
        print('nan appear xi' , xi_vi_nan)

    psi_vi_mu = fenzi_psi / fenmu_psi
    psi_vi_mu = psi_vi_mu / np.sum(psi_vi_mu , axis = 1)[: , None]
    psi_vi_sigma = sigma_w / fenmu_psi
    psi_vi_mu_rmse = np.sqrt(np.average((psi_vi_mu - psi_vi_mu_old) ** 2))
    psi_vi_sigma_rmse = np.sqrt(np.average((psi_vi_sigma - psi_vi_sigma_old) ** 2))
    psi_vi_nan = np.isnan(psi_vi).sum()
    if psi_vi_nan > 0:
        print(psi_vi)
        print('nan appear psi' , psi_vi_nan)

    y_vi = np.exp(y_vi_exps)
    y_vi = y_vi / np.sum(y_vi , axis=2)[: , : , None]
    y_vi_rmse = np.sqrt(np.average((y_vi - y_vi_old) ** 2))
    y_vi_nan = np.isnan(y_vi).sum()
    if y_vi_nan > 0:
        print(y_vi)
        print('nan appear y' , y_vi_nan)

    # update lambda_vi
    print(datetime.datetime.now(), 'update lambda_vi begin:')
    for k in range(K):
        for f in range(F):
            lambda_vi_mu[k][f] = sigma_lambda[f] * np.sum(np.multiply(alpha_vi_old[: , k] , X[: , f]))
        lambda_vi_sigma[k] = sigma_lambda.copy()
    lambda_vi_mu_rmse = np.sqrt(np.average((lambda_vi_mu - lambda_vi_mu_old) ** 2))
    lambda_vi_sigma_rmse = np.sqrt(np.average((lambda_vi_sigma - lambda_vi_sigma_old) ** 2))
    lambda_vi_mu_nan = np.isnan(lambda_vi_mu).sum()
    if lambda_vi_mu_nan > 0:
        print(lambda_vi_mu)
        print('nan appear lambda_vi_mu')


    # update alpha_vi
    print(datetime.datetime.now(), 'update alpha_vi begin:')
    for r in range(R):
        for k in range(K):
            alpha_vi[r][k] = 1/(-Digamma_theta_vi_R_K_subtract_sum[r][k] - np.sum(np.multiply(X[r , :] , lambda_vi_mu_old[k , :])))
    #alpha_vi = alpha_vi / np.sum(alpha_vi, axis=1)[: , None]
    alpha_vi_nan = np.isnan(alpha_vi).sum()
    if alpha_vi_nan > 0:
        print(alpha_vi)
        print('nan appear alpha')
    alpha_vi_rmse = np.sqrt(np.average((alpha_vi - alpha_vi_old) ** 2))


    # update theta_vi
    print(datetime.datetime.now(), 'update theta_vi begin:')
    theta_vi = alpha_vi_old + np.sum(z_vi_old , axis=1) + np.sum(y_vi_old , axis=1)
    #theta_vi = theta_vi / np.sum(theta_vi, axis=1)[:, None]
    theta_vi_nan = np.isnan(theta_vi).sum()
    if theta_vi_nan > 0:
        print(theta_vi)
        print('nan appear theta')
    theta_vi_rmse = np.sqrt(np.average((theta_vi - theta_vi_old) ** 2))




    # update z_vi
    print(datetime.datetime.now(), 'update z_vi begin:')
    for r in range(R):
        for n in range(N):
            i = T[r][n]
            for k in range(K):
                temp = Digamma_phi_vi_K_I_subtract_sum[k][i]  + Digamma_theta_vi_R_K_subtract_sum[r][k]
                z_vi[r][n][k] = np.exp(temp)
    z_vi = z_vi / np.sum(z_vi, axis=2)[:, :, None]
    z_vi_nan = np.isnan(z_vi).sum()
    if z_vi_nan > 0:
        print(z_vi)
        print('nan appear z')
    z_vi_rmse = np.sqrt(np.average((z_vi - z_vi_old) ** 2))


    # judge convergence

    save(count)
    with open('rmse.txt', 'a') as f:
        f.write(str(datetime.datetime.now()) + '\t' + str(phi_vi_rmse) + '\t' + str(pi_vi_rmse) + '\t' + str(xi_vi_mu_rmse) + '\t' + str(xi_vi_sigma_rmse) + '\t' + str(psi_vi_mu_rmse) + '\t' + str(psi_vi_sigma_rmse) + '\t' + str(y_vi_rmse) + '\t' + str(lambda_vi_mu_rmse) + '\t' + str(lambda_vi_sigma_rmse) + '\t' + str(alpha_vi_rmse) + '\t' + str(theta_vi_rmse) + '\t' + str(z_vi_rmse) + '\n')

    # judge convergence
    #if phi_vi_rmse > Threshold or pi_vi_rmse > Threshold or xi_vi_mu_rmse > Threshold or xi_vi_sigma_rmse > Threshold or c_vi_mu_rmse > Threshold or c_vi_sigma_rmse > Threshold or lambda_vi_mu_rmse > Threshold or lambda_vi_sigma_rmse > Threshold or alpha_vi_rmse > Threshold or theta_vi_rmse > Threshold or y_vi_rmse > Threshold or z_vi_rmse > Threshold or psi_vi_rmse > Threshold or l_vi_mu_rmse > Threshold or l_vi_sigma_rmse > Threshold:
    if theta_vi_rmse > 800 or alpha_vi_rmse > 0.1:
        return False
    else:
        return True


def Mstep(count):
    global beta
    global epsilon
    beta_old = beta.copy()
    epsilon_old = epsilon.copy()

    # update beta
    print(datetime.datetime.now(), 'update beta begin:')
    Digamma_beta_I = scipy.special.digamma(beta_old)
    Digamma_beta_sum = scipy.special.digamma(np.sum(beta_old))
    Trigamma_beta_I = scipy.special.polygamma(1, beta_old)
    Trigamma_beta_sum = scipy.special.polygamma(1, np.sum(beta_old))
    Digamma_phi_K_I = np.sum(scipy.special.digamma(phi_vi), axis=0) / K
    Digamma_phi_K_sum = np.sum(scipy.special.digamma(np.sum(phi_vi, axis=1))) / K
    for i in range(I):
        fenzi = Digamma_beta_sum - Digamma_beta_I[i] + Digamma_phi_K_I[i] - Digamma_phi_K_sum
        fenmu = Trigamma_beta_sum
        tidu = (I - 1) * fenzi / fenmu + fenzi / (fenmu - Trigamma_beta_I[i])
        beta[i] += Learning_rate * tidu

    # update epsilon
    print(datetime.datetime.now(), 'update epsilon begin:')
    Digamma_epsilon_Q = scipy.special.digamma(epsilon_old)
    Digamma_epsilon_sum = scipy.special.digamma(np.sum(epsilon_old))
    Trigamma_epsilon_Q = scipy.special.polygamma(1, epsilon_old)
    Trigamma_epsilon_sum = scipy.special.polygamma(1, np.sum(epsilon_old))
    Digamma_pi_K_Q = np.sum(scipy.special.digamma(pi_vi), axis=0) / K
    Digamma_pi_K_sum = np.sum(scipy.special.digamma(np.sum(pi_vi, axis=1))) / K
    for q in range(Q):
        fenzi = Digamma_epsilon_sum - Digamma_epsilon_Q[q] + Digamma_pi_K_Q[q] - Digamma_pi_K_sum
        fenmu = Trigamma_epsilon_sum
        tidu = ((Q - 1) * fenzi / fenmu + fenzi / (fenmu - Trigamma_epsilon_Q[q])) / 100000
        epsilon[q] += Learning_rate * tidu
    save(count)

    # return whether convergence
    beta_rmse = np.sqrt(np.average((beta - beta_old) ** 2))
    print('RMSE of beta:', beta_rmse)
    epsilon_rmse = np.sqrt(np.average((epsilon - epsilon_old) ** 2))
    print('RMSE of epsilon:', epsilon_rmse)
    #if beta_rmse > Threshold or epsilon_rmse > Threshold:
    if beta_rmse > 10 or epsilon_rmse > 10:
        return False
    else:
        return True


def save(count=0):
    count = str(count)
    np.savetxt('result/result' + count + '/phi_vi.txt', phi_vi, fmt='%.8f', delimiter='\t')
    np.savetxt('result/result' + count + '/pi_vi.txt', pi_vi, fmt='%.8f', delimiter='\t')
    np.savetxt('result/result' + count + '/xi_vi_mu.txt', xi_vi_mu, fmt='%.8f', delimiter='\t')
    np.savetxt('result/result' + count + '/xi_vi_sigma.txt', xi_vi_sigma, fmt='%.8f', delimiter='\t')
    np.savetxt('result/result' + count + '/psi_vi_mu.txt', psi_vi_mu, fmt='%.8f', delimiter='\t')
    np.savetxt('result/result' + count + '/psi_vi_sigma.txt', psi_vi_sigma, fmt='%.8f', delimiter='\t')
    np.savetxt('result/result' + count + '/lambda_vi_mu.txt', lambda_vi_mu, fmt='%.8f', delimiter='\t')
    np.savetxt('result/result' + count + '/lambda_vi_sigma.txt', lambda_vi_sigma, fmt='%.8f', delimiter='\t')
    np.savetxt('result/result' + count + '/alpha_vi.txt', alpha_vi, fmt='%.8f', delimiter='\t')
    np.savetxt('result/result' + count + '/theta_vi.txt', theta_vi, fmt='%.8f', delimiter='\t')
    y_vi_max_index = np.argmax(y_vi, axis=2)
    np.savetxt('result/result' + count + '/y_vi_max_index.txt', y_vi_max_index, fmt='%d', delimiter='\t')
    z_vi_max_index = np.argmax(z_vi, axis=2)
    np.savetxt('result/result' + count + '/z_vi_max_index.txt', z_vi_max_index, fmt='%d', delimiter='\t')

    np.savetxt('result/result' + count + '/b.txt', b, fmt='%.8f', delimiter='\t')
    np.savetxt('result/result' + count + '/sigma_lambda.txt', sigma_lambda, fmt='%.8f', delimiter='\t')
    np.savetxt('result/result' + count + '/sigma_xi.txt', sigma_c, fmt='%.8f', delimiter='\t')
    np.savetxt('result/result' + count + '/sigma_psi.txt', sigma_psi, fmt='%.8f', delimiter='\t')
    with open('result/result' + count + '/sigma_w.txt', 'w') as f:
        f.write(str(sigma_w))
    np.savetxt('result/result' + count + '/beta.txt', beta, fmt='%.8f', delimiter='\t')
    np.savetxt('result/result' + count + '/epsilon.txt', epsilon, fmt='%.8f', delimiter='\t')


if __name__ == "__main__":
    RMSE = 1000
    iteration = 1
    save(9)
    with open('rmse.txt', 'w') as f:
        f.write(
            'TIME \t phi_vi_rmse \t pi_vi_rmse \t xi_vi_mu_rmse \t xi_vi_sigma_rmse \t psi_vi_mu_rmse \t psi_vi_sigma_rmse \t y_vi_rmse \t lambda_vi_mu_rmse \t lambda_vi_sigma_rmse \t alpha_vi_rmse \t theta_vi_rmse \t z_vi_rmse \n')
    while iteration < ITER:
        print('begin ' + str(iteration) + 'th iteration!')
        VI_convergence = False
        print('E-step begin:', datetime.datetime.now())
        count = 0
        while VI_convergence == False:
            VI_convergence = Estep(count)
            count += 1
            print(iteration, 'E:', count)
        count = 0
        Model_convergence = False
        print('M-step begin:', datetime.datetime.now())

        while Model_convergence == False:
            Model_convergence = Mstep(count)

            xi_vi = xi_vi_mu * xi_vi_mu + 2 * xi_vi_sigma
            psi_vi = psi_vi_mu * psi_vi_mu + psi_vi_sigma

            # update b
            print(datetime.datetime.now(), 'update b begin:')
            b = np.sum(xi_vi_mu, axis=0) / Q
            # update sigma_lambda^
            print(datetime.datetime.now(), 'update sigma_lambda^2 begin:')
            sigma_lambda = np.sum(lambda_vi_mu * lambda_vi_mu + lambda_vi_sigma, axis=0) / K

            '''
            # update sigma_w^2
            sigma_w = 0
            print(datetime.datetime.now(), 'update sigma_w^2 begin:')
            for r in range(R):
                for m in range(M_r[r]):
                    for d in range(D_rm[r][m]):
                        v = W[r][m][d]
                        belong_Q = W_Q[r][m][d]
                        for q in belong_Q:
                            sigma_w += word_fres[v][q] ** 2
                            sigma_w -= 2 * word_fres[v][q] * np.sum(np.multiply(xi_vi_mu[q , :] , psi_vi_mu[: , v]))
                            sigma_w += np.sum(np.multiply(xi_vi[q , :] , psi_vi[: , v]))
            print('sigma_w' , sigma_w)
            sigma_w = sigma_w / (R * M_mean * D_mean)
            '''

            # update sigma_psi
            print(datetime.datetime.now(), 'update sigma_psi begin:')
            sigma_psi= np.sum(psi_vi, axis=1) / V

            save(count)
            count += 1
            print(iteration, 'M:', count)

        if Estep(count) == True:
            break
        else:
            iteration += 1
