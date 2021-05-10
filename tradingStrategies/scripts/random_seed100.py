import numpy as np
import pandas as pd

# using complete dataframe
def run(df):
    res = []
    current_stock = 0
    lim = 100
    np.random.seed(100)

    for i in range(len(df)):
        d = {}
        d["actions"] = np.random.choice(['sell','buy',''],p=[.15,.1,.75])
        if d["actions"].lower() == 'sell':
            d["quantity"] = np.random.randint(0,current_stock,1)[0]
        elif d["actions"].lower() == 'buy':
            d["quantity"] = np.random.randint(0,lim,1)[0]
            current_stock += d["quantity"]
        else:
            d["quantity"] = ''
        res.append(d)

    return res


current_stock = 0
lim = 100
np.random.seed(100)
# gets the stream of data input
def run_live(df):
    global current_stock,lim
    d = {}
    d["actions"] = np.random.choice(['sell','buy',''],p=[.15,.1,.75])
    if d["actions"].lower() == 'sell':
        d["quantity"] = np.random.randint(0,current_stock,1)[0]
    elif d["actions"].lower() == 'buy':
        d["quantity"] = np.random.randint(0,lim,1)[0]
        current_stock += d["quantity"]
    else:
        d["quantity"] = ''
    
    return d