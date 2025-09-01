# import code here
from precode import *
import numpy as np
import pandas as pd
%matplotlib inline
import matplotlib.pyplot as plt

data = np.load('AllSamples.npy')

initial_centers = {}
for k in range(2, 11):
    centers = initial_S1("4114", k)  # please replace 0111 with your last four digit of your ID
    initial_centers[k] = centers

datt = pd.DataFrame(data, columns=['x', 'y'])
pr = [[1,1], [3, 2], [5, 7]]
pi = [[1,1], [2,2]]



def cluster(dat, ic, k):
    carray = []
    for i in range(len(dat)):
        nv = []
        for j in range(len(ic)):
            v = ((dat[i][0] - ic[j][0]) ** 2) + ((dat[i][1] - ic[j][1]) ** 2)
            nv.append(v)
        k = nv.index(min(nv))
        carray.append(k)
    return carray

def new_cents(cluster_array, dat, k):
    
    new_vals = []

    for i in range(k):
        xmean = 0 
        ymean = 0
        ind = []
        for c, val in enumerate(cluster_array):
            if val == i:
                ind.append(c)
        for j in ind:
            xmean = xmean + dat[j][0]
            ymean = ymean + dat[j][1]
        xmean = xmean / len(ind)
        ymean = ymean / len(ind)
        new_vals.append([float(xmean), float(ymean)])
    return new_vals

def kmean(dat, ic, k):
    clust = cluster(dat, ic, k)
    cent = new_cents(clust, dat, k)
    #print(cent)
    if cent == ic:
        #print('made it')
        #print(cent)
        return cent
    else:
        return kmean(dat, cent, k)
def loss(dat, cen, k):
    cl = cluster(dat, cen, k)
    summ = 0
    for s in range(k):
        for i, val in enumerate(cl):
            if val == s:
                su = ((data[i][0] - cen[s][0]) ** 2) + ((data[i][1] - cen[s][1]) ** 2)
                summ = summ + su
    return summ



j = kmean(pr, pi, 2)
#print(j)
h = cluster(pr, pi, 2)
#print(h)
h = new_cents(h, pr, 2)
#print(h)
f = initial_centers[2]
#print(initial_centers[2][1][0])
#print(f)
c_val = []

### TEST FUNCTION: test_question1
# DO NOT REMOVE THE ABOVE LINE
for i in range(2, 11):
    li = []
    for d in range(i):
        x = initial_centers[i][d][0]
        y = initial_centers[i][d][1]
        li.append((x, y))
    v = kmean(data, li, i)
    c_val.append(v)
    print(v)

### TEST FUNCTION: test_question2
# DO NOT REMOVE THE ABOVE LINE

losses = []
for i in range(2, 11):
    b = loss(data, c_val[i - 2], i)
    losses.append((i, b))
    print(b)

for i in range(2, 11):
    datt[f'{i}'] = cluster(data, c_val[i - 2], i)
    plt.scatter(datt['x'], datt['y'], c=datt[f'{i}'])
    plt.title(f'{i} Clusters')
    plt.show()
