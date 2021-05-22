import numpy as np
import pandas as pd

# using complete dataframe
def run(df):
    res = []
    print("good")
    current_stock = 0
    lim = 10
    np.random.seed(150)

    for i in range(len(df)):
        d = {}
        d["actions"] = np.random.choice(['buy','sell',''],p=[.15,.1,.75])
        d["quantity"] = 0
        
        if d["actions"].lower() == 'sell' and current_stock > 0:
            d["quantity"] = np.random.randint(0,current_stock,1)[0]
            current_stock -= d["quantity"]
        elif d["actions"].lower() == 'buy':
            d["quantity"] = np.random.randint(0,lim,1)[0]
            current_stock += d["quantity"]
        res.append(d)

    return res


current_stock = 0
lim = 100
np.random.seed(100)
# gets the stream of data input
def run_live(df):
    # edit this code

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