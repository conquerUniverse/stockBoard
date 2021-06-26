# ------------------- Insturctions -----------------
# using complete dataframe
# return a dataframe with columns
# timestamp ,actions ,quantity
# timestamp -> date in YYYY-MM-DD
# actions -> ['buy','sell'] @string format
# quantity -> integer value
# if you dont want to do any action .. you can skip that dataframe.

import numpy as np
import pandas as pd


class RandomStrategy:
    def __init__(self):
        pass

    def run(self, df):
        res = []
        current_stock = 0
        lim = 789
        for i in range(len(df)):
            d = {}
            d["actions"] = np.random.choice(["buy", "sell", ""], p=[0.15, 0.1, 0.75])
            d["quantity"] = 0
            d["timestamp"] = df.iloc[i]["timestamp"]

            if d["actions"].lower() == "sell" and current_stock > 0:
                d["quantity"] = np.random.randint(0, current_stock, 1)[0]
                current_stock -= d["quantity"]
            elif d["actions"].lower() == "buy":
                d["quantity"] = np.random.randint(0, lim, 1)[0]
                current_stock += d["quantity"]
            else:
                continue
            res.append(d)

        return res


rs = RandomStrategy()
run = rs.run
