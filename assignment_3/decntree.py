#16EE35002
#Anuraag Bhattacharya
# Assignment number-1

import numpy as np
import math
import csv
import copy


def entropy(n_p,n_n):
    p=n_p/(n_p+n_n)
    n=1-p
    if p==0 or n==0: return 0
    return -(p*math.log(p,2)+n*math.log(n,2))


def gain(S,attr,attr_idx):
    s1=np.sum(S,axis=0)
    s1_n=s1[-1]
    s1_p=S.shape[0]-s1_n
#     if s1_n==0:return -1
#     if s1_p==0:return -2
    ent1=entropy(s1_p,s1_n)
    Sm=0
    for i in range(1,len(attr[attr_idx])):
        S_new=np.where(S[:,attr_idx]==i-1)
        S_new=S[S_new]
        s2=np.sum(S_new,axis=0)
        n=s2[-1]
        p=S_new.shape[0]-n
        Sm+=(S_new.shape[0]/S.shape[0])*entropy(p,n)
    return ent1-Sm


class tree:
    def __init__(self,root,attr,val):
        self.root=root
        self.attr=attr
        self.val=val
        self.children=[]
        
    def __str__(self):
        return str(self.val)+'\n'


root=tree(-1,[],-1)
root1=root

root=tree(-1,[],-1)
root1=root

def decn_tree(L,attr,idx,root):
    s1=np.sum(L,axis=0)
    s1_n=s1[-1]
    s1_p=L.shape[0]-s1_n
    if s1_n==0:
        root.val=0
        print ('\t'*(len(attr)-len(idx)-1)+':yes')
        return 1
    if s1_p==0:
        root.val=1
        print ('\t'*(len(attr)-len(idx)-1)+':no')
        return -1
    if len(idx)==0:
        if s1_p>s1_n:
            root.val=0
            print('\t'*(len(attr)-len(idx)-1)+':yes')
            return 1
        else:
            root.val=1
            print('\t'*(len(attr)-len(idx)-1)+':no')
            return -1
    maxid=idx[0]
    id=0
    max_g=gain(L,attr,idx[0])
    for i in range(1,len(idx)):
        g=gain(L,attr,idx[i])
        if g>max_g:
            maxid=idx[i]
            max_g=g
            id=i
    root.val=maxid
    root.attr=[k for k in range(len(attr[maxid])-1)]   
    cnt=0
    for i in range(1,len(attr[maxid])):
        print(('\t'*(len(attr)-len(idx)-1))+attr[maxid][0]+'='+attr[maxid][i])
        S_new=np.where(L[:,maxid]==i-1)
        S_new=L[S_new]
        idx.remove(maxid)
        new=tree(root,[],-1)
        root.children.append(new)
        cnt+=decn_tree(S_new,attr,idx,new)
        idx.insert(id,maxid)
    if cnt==(len(attr[maxid])-1):
        print('\t'*(len(attr)-len(idx)-1)+':yes')
        return 1
    elif cnt==-(len(attr[maxid])-1):
        print('\t'*(len(attr)-len(idx)-1)+':no')
        return -1
    return 0
    
