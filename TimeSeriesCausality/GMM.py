import pandas as pd
pd.options.display.max_rows = 10
import matplotlib
import matplotlib.pyplot as plt
matplotlib.style.use('ggplot')
# some example data
import numpy as np
import pandas
import random
import statsmodels.api as sm
from statsmodels.tsa.api import VAR, DynamicVAR
def GMM(k,n):
    w=np.random.rand(1,k)
    wsum=np.sum(w)
    w=w/wsum
    wsumt=0
    #mu=2*np.random.rand(1,k)-1
    level=np.zeros(k)
    #sigma=10*np.random.rand(1,k)
    mu = np.random.rand(1, k) - 0.5
    sigma = 0.5 * np.random.rand(1, k)
    X=[]
    for ii in range(k):
        wsumt+=w[0][ii]
        level[ii]=wsumt
    #for ij in range(k-1):
        #level[ij+1]=level[ij]+level[ij+1]
    for ik in range(n):
        lev=np.random.random_sample()
        count=0
        for alp in range(k):
            if lev <level[alp]:
                count=alp
                break
        x=np.random.normal(mu[0][count],sigma[0][count],1)
        X.extend(x.tolist())
    return X


def GMMGranger(k,t,n):
    bet=0
    yes=0
    while bet<=n-1:
        xseries=GMM(k,t)
        yseries=GMM(k+3,t)
        data=pd.DataFrame([xseries,yseries]).transpose()
        model=VAR(np.asarray(data))
        try:
            results=model.fit(maxlags=15,ic='aic',trend='nc')
        except:
            continue
        bet+=1
        if results.test_causality(0,1,kind='wald').summary().data[1][2]>0.05:
            if results.test_causality(1,0,kind='wald').summary().data[1][2]>0.05:
                yes+=1
    return float(yes)/n

#accuracy=GMMGranger(5,200,100)
#print accuracy