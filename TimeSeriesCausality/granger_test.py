import pandas as pd
pd.options.display.max_rows = 10
import matplotlib
import matplotlib.pyplot as plt
matplotlib.style.use('ggplot')
# some example data
import numpy as np
import pandas
import statsmodels.api as sm
from statsmodels.tsa.api import VAR, DynamicVAR


def granger(cause,effect,lag):
    data = pd.DataFrame({'cause':cause,'effect':effect})
    return_vaule = 1
    #data=pd.read_csv('data/test.txt',sep='\t')
    model = VAR(data)
    try:
        if lag == -1:
            results = model.fit(maxlags=15, ic='aic', trend='nc')
        else:
            results = model.fit(lag)
        x = results.test_causality('effect', 'cause', kind='wald').summary().data
        return_vaule = x[1][2]
    except Exception:
        print 'error'
    return return_vaule


