# encoding: utf-8
"""

机器学习经典算法之PageRank
https://www.cnblogs.com/jpcflyer/p/11180263.html

PageRank算法学习及使用
https://blog.csdn.net/liujh845633242/article/details/103504499

PageRank算法（二）
https://blog.csdn.net/weixin_42168614/article/details/87929326

从PageRank到反欺诈与TextRank
https://zhuanlan.zhihu.com/p/219759280

浅谈PageRank算法
https://zhuanlan.zhihu.com/p/197877312


[python pagerank实现的工具包，原理简介](https://blog.csdn.net/a19990412/article/details/94159407)

"""


import numpy as np
import random


def create_data(N, alpha=0.5): # random > alpha, then here is a edge.
    G = np.zeros((N, N))
    for i in range(N):
        for j in range(N):
            if i == j:
                continue
            if random.random() < alpha:
                G[i][j] = 1
    return G

G = create_data(10)


def GtoM(G, N):
    M = np.zeros((N, N))
    for i in range(N):
        D_i = sum(G[i])
        if D_i == 0:
            continue
        for j in range(N):
            M[j][i] = G[i][j] / D_i # watch out! M_j_i instead of M_i_j
    return M

M = GtoM(G, 10)



# Google Formula
def PageRank(M, N, T=300, eps=1e-6, beta=0.8):
    R = np.ones(N) / N
    teleport = np.ones(N) / N
    for time in range(T):
        R_new = beta * np.dot(M, R) + (1-beta)*teleport
        if np.linalg.norm(R_new - R) < eps:
            break
        R = R_new.copy()
    return R_new


values = PageRank(M, 10, T=2000)
values
'''
array([0.09815807, 0.09250429, 0.08376235, 0.09300133, 0.09324628,
       0.10108776, 0.09855127, 0.13019363, 0.12458992, 0.0849051 ])
'''


