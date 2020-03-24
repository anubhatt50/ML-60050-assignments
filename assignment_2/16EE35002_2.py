#16EE35002
#Anuraag Bhattacharya
# Assignment number-2

import numpy as np
import math
import csv


L=[]

flag=0

s=input("Enter training csv file path:")

with open(s,'rt')as f:
    data = csv.reader(f)
    for row in data:
        if flag==0:
            flag=1
        else:
            row=row[0].split(',')
            for i in range(len(row)):
                row[i]=int(row[i])
            L.append(row)
            
L=np.array(L)


def prob(L,attr,cls,n_class):
    L2=L[np.where(L[:,0]==cls)]
    den=len(L2)+n_class
    p=1
    for i in range(len(attr)):
        num=len(np.where(L2[:,i+1]==attr[i])[0])+1
        p*=(num/den)
    return p


def bayes(L,attr,n_class):
    apost=[]
    den=len(L)
    for i in range(n_class):
        num=len(np.where(L[:,0]==i)[0])
        apost.append(num/den)
    p=[]
    for i in range(n_class):
        p.append(prob(L,attr,i,n_class)*apost[i])
    return(p.index(max(p)))

L_test=[]

flag=0

s2=input("Enter test csv file path:")

with open(s2,'rt')as f2:
    data = csv.reader(f2)
    for row in data:
        if flag==0:
            flag=1
        else:
            row=row[0].split(',')
            for i in range(len(row)):
                row[i]=int(row[i])
            L_test.append(row)
            
L_test=np.array(L_test)

acc=0

for i in range(len(L_test)):
    if bayes(L,L_test[i,1::],2)==L_test[i,0]: acc+=1
        
acc=acc/len(L_test)

print("Accuracy: {0:.4f} %".format(acc*100))



