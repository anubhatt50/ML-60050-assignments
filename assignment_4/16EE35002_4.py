#16EE35002
#Anuraag Bhattacharya
# Assignment number-4

import numpy as np
import math
import csv
import copy
import sys
import time

L_data=[]
L_label=[]
attr=[]

flag=0

s=input("Enter csv file path:")

with open(s,'rt')as f:
    data = csv.reader(f)
    for row in data:
        try:
            L_data.append([float(row[i]) for i in range(4)])
            L_label.append(row[4])
            if row[4] not in attr:
                attr.append(row[4])
        except IndexError:
            break
L_data=np.array(L_data)
L_label=np.array(L_label)

def euc_dist(x,y):
    return np.linalg.norm(x-y)

def clustering(seed,L_data):
    cluster=np.zeros((L_data.shape[0]))
    for i in range(L_data.shape[0]):
        min_dist=999999
        min_dist_ind=-1
        for j in range(3):
            dist=euc_dist(L_data[i],seed[j])
            if dist<min_dist:
                min_dist=dist
                min_dist_ind=j
        cluster[i]=min_dist_ind
    return cluster


def cluster_mean(cluster,L_data):
    K=len(np.unique(cluster))
    mean=np.zeros((K,L_data.shape[1]))
    num=[0 for i in range (K)]
    for i in range (L_data.shape[0]):
        mean[int(cluster[i])]+=L_data[i]
        num[int(cluster[i])]+=1
    for i in range(K):
        mean[i]/=num[i]
    return mean


K=3
iter=10
num_attr=4

seed=np.zeros((K,num_attr))

rand=np.random.choice(range(L_data.shape[0]), K, replace=False)

for i in range(K):
    seed[i]=L_data[rand[i]]

for i in range(iter):
    cluster=clustering(seed,L_data)
    seed=cluster_mean(cluster,L_data)


def jaccard(x,y):
    inter=0
    for i in range(len(x[0])):
        if x[0][i] in y[0]:
            inter+=1
    union=len(x[0])+len(y[0])-inter
    return inter/union


jac_pred=[[] for i in range(K)]
for i in range(K):
    jac_pred[i].append(np.where(cluster==i)[0])
    
jac_lbl=[[] for i in range(K)]
for i in range(K):
    jac_lbl[i].append(np.where(L_label==attr[i])[0])


for i in range(K):
    for j in range(K-i-1):
        if np.mean(jac_lbl[j])>np.mean(jac_lbl[j+1]):
            jac_lbl[j], jac_lbl[j+1]=jac_lbl[j+1], jac_lbl[j]
            
for i in range(K):
    for j in range(K-i-1):
        if np.mean(jac_pred[j])>np.mean(jac_pred[j+1]):
            jac_pred[j], jac_pred[j+1]=jac_pred[j+1], jac_pred[j]


for i in range(K):
    x=jaccard(jac_lbl[i],jac_pred[i])
    print("Jaccard score of cluster "+str(i+1)+":",x)



