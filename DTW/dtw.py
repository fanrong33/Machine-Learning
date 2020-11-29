# encoding: utf-8
"""
"""

import sys

def Distance(x,y):
    return abs(x-y)

def Dtw(X,Y):
    Lx=len(X)
    Ly=len(Y)
    D=[[sys.maxsize for i in range(Lx)]for j in range(Ly)]
    minD=0
    j=0
    k=0
    path=[(0,0)]
    for i in range(Lx+Ly):
        if (j == Ly-1) and (k == Lx-1):
            break
        elif (j==Ly-1) and (k != Lx-1):
            k += 1
            D[j][k]=D[j][k-1]+Distance(Y[j],X[k])
        elif (j != Ly-1) and (k == Lx-1):
            j += 1
            D[j][k]=D[j-1][k]+Distance(Y[j],X[k])
        else:
            if j==0 and k==0:
                D[j][k]=Distance(Y[j],X[k])
            D[j+1][k]=Distance(Y[j+1],X[k])+D[j][k]
            D[j][k+1]=Distance(Y[j],X[k+1])+D[j][k]
            D[j+1][k+1]=Distance(Y[j+1],X[k+1])+D[j][k]
            if(D[j+1][k]<D[j][k+1]):
                minD=D[j+1][k]
                if(minD>D[j+1][k+1]):
                    j += 1
                    k += 1
                else:
                    j += 1
            else:
                minD=D[j][k+1]
                if(minD>D[j+1][k+1]):
                    j += 1
                    k += 1
                else:
                    k += 1
        path.append((k,j))
        minD=D[j][k]
    return minD # ,path

def dtw(X,Y):
    Lx=len(X)
    Ly=len(Y)
    path=[]
    M=[[Distance(X[i],Y[j]) for i in range(Lx)]for j in range(Ly)]
    D=[[0 for i in range(Lx+1)]for j in range(Ly+1)]
    D[0][0]=0
    for i in range(1,Lx+1):
        D[0][i]=sys.maxsize
    for j in range(1,Ly+1):
        D[j][0]=sys.maxsize
    for i in range(1,Ly+1):
        for j in range(1,Lx+1):
            D[i][j]=M[i-1][j-1]+min(D[i-1][j],D[i-1][j-1],D[i][j-1])
    minD=D[Ly][Lx]
    return minD


import qdata


df1 = qdata.get_price('601187.XSHG', start_date='2020-11-27 09:25:00', end_date='2020-11-27 15:00:00', frequency='1m')
df2 = qdata.get_price('600318.XSHG', start_date='2020-11-27 09:25:00', end_date='2020-11-27 15:00:00', frequency='1m')
df3 = qdata.get_price('601995.XSHG', start_date='2020-11-27 09:25:00', end_date='2020-11-27 15:00:00', frequency='1m')
# pct_change?
exit()
d1 = df1.close.values
d2 = df2.close.values
d3 = df3.close.values


# print(Dtw(x, y))
print(Dtw(d1, d2))
print(Dtw(d1, d3))
print(Dtw(d2, d3))



import numpy as np
from scipy.spatial.distance import euclidean

from fastdtw import fastdtw

# x = np.array([[1,1], [2,2], [3,3], [4,4], [5,5]])
# y = np.array([[2,2], [3,3], [4,4]])
# distance, path = fastdtw(x, y, dist=euclidean)
# print(distance)

distance, path = fastdtw(d1, d2, dist=euclidean)
print(distance)
distance, path = fastdtw(d1, d3, dist=euclidean)
print(distance)
distance, path = fastdtw(d2, d3, dist=euclidean)
print(distance)








