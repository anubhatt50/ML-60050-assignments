#16EE35002
#Anuraag Bhattacharya
# Assignment number-3

import numpy as np
import math
import csv
import copy
import sys
import time
import random
from decntree import tree, decn_tree


L=[]
attr=[]

flag=0

s=input("Enter training csv file path:")

with open(s,'rt')as f:
    data = csv.reader(f)
    for row in data:
        if flag==0:
            for i in range(len(row)):
                attr.append([row[i]])
            flag=1
        else:
            for i in range(len(row)):
                if row[i] not in attr[i]:
                    attr[i].append(row[i])
            L.append(row)
            
val={}
for i in range(len(attr)):
    for j in range(1,len(attr[i])):
        val[attr[i][j]]=j-1


for i in range(len(L)):
    for j in range(len(L[i])):
        L[i][j]=val[L[i][j]]
        
L=np.array(L)

W=np.array([1/len(L) for i in range (len(L))])

def error(W,Y):
    E=np.sum(W*Y)
    E=E/len(W)
    return E


def alpha(E):
    return 0.5*math.log((1-E)/E)


def update_wt(W,Y):
    E=error(W,Y)
    a=alpha(E)
    W_new=np.array([W[i]*math.exp(-((Y[i]*2)-1)*a) for i in range (len(W))])
    W_new=W_new/np.sum(W_new)
    return W_new,a


def select_data(L,W):
    W_cum=np.cumsum(W)
    L_new=[]
    for i in range(len(L)):
        rand_num=random.random()
        x=np.argwhere(W_cum>rand_num)
        L_new.append(L[x[0][0]])
    L_new=np.array(L_new)
    return(L_new)


def score(root,L):
    scores=[]
    for i in range(len(L)):
        root2=copy.deepcopy(root)
        v=root.val
        for j in range(len(L[i])-1):
            if len(root2.children)==0:break
            at=L[i][v]
            root2=root2.children[at]
            v=root2.val
        if root2.val==L[i][-1]: scores.append(1)
        else: scores.append(0)
    return np.array(scores)


L_test=[]

s2=input("Enter test csv file path:")

with open(s2,'rt')as f:
    data = csv.reader(f)
    for row in data:
        L_test.append(row)
        
for i in range(len(L_test)):
    for j in range(len(L_test[i])):
        L_test[i][j]=val[L_test[i][j]]
        
L_test=np.array(L_test)

iters=3
test_sc=np.zeros((len(L_test)))

for i in range(iters):
    L_new=select_data(L,W)
    root=tree(-1,[],-1)
    print('ITERATION '+str(i+1)+':')
    decn_tree(L_new,attr,[0,1,2],root)
    sc=score(root,L_new)
    W,a=update_wt(W,sc)
    test_sc+=a*(2*score(root,L_test)-1)  
    
test_sc[test_sc>0]=1
test_sc[test_sc<0]=0


acc=np.logical_not(np.logical_xor(L_test[:,-1],test_sc))
print ("Accuracy:",(sum(acc)/len(acc))*100,"%")

