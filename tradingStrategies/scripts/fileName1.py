import numpy as np
import pandas as pd

# using complete dataframe
class RandomStrategy:
    def __init__(self,seed):
        pass
        # np.random.seed(seed)

    def run(self,df):
        res = []
        current_stock = 0
        lim = 100
        for i in range(len(df)):
            d = {}
            d["actions"] = np.random.choice(['buy','sell',''],p=[.15,.1,.75])
            d["quantity"] = 0
            d["timestamp"] = df.iloc[i]['timestamp']

            if d["actions"].lower() == 'sell' and current_stock > 0:
                d["quantity"] = np.random.randint(0,current_stock,1)[0]
                current_stock -= d["quantity"]
            elif d["actions"].lower() == 'buy':
                d["quantity"] = np.random.randint(0,lim,1)[0]
                current_stock += d["quantity"]
            else:
                continue  
            res.append(d)

        return res

rs = RandomStrategy(5)
run = rs.run