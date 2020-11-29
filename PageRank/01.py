# encoding: utf-8
"""


"""


def create(q,graph,N):
    #compute Probability Matrix
    L = [[(1-q)/N]*N for i in range(N)]
    for node,edges in enumerate(graph):
        num_edge = len(edges)
        for each in edges:
            L[each][node] += q/num_edge
    return L
def transform(A):
    n,m = len(A),len(A[0])
    new_A = [[A[j][i] for j in range(n) ] for i in range(m)]
    return new_A
def mul(A,B):
    n = len(A)
    m = len(B[0])
    B = transform(B)
    next = [[0]*m for i in range(n)]
    for i in range(n):
        row = A[i]
        for j in range(m):
            col = B[j]
            next[i][j] = sum([row[k]*col[k] for k in range(n)])
    return next
def power(A,N):
    n = len(A)
    assert(len(A[0])==n)
    final_ans,temp = A,A
    N-=1
    while N>0:
        if N&1:
            final_ans = mul(final_ans,temp)
        temp = mul(temp,temp)
        N >>=1
    return final_ans
def PageRank(q,graph,N):
    X = [[1] for i in range(N)]
    A = create(q,graph,N)
    X = mul(power(A,20),X)
    return X



print(PageRank(0.85,[[1,2],[2],[0]],3))
# [[1.1633753188067963], [0.6444184237734443], [1.1922062574197603]]



