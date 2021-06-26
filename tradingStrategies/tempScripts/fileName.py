import numpy as np
import pandas as pd
from ta.momentum import RSIIndicator


class RSIStrategy:
    def __init__(self):
        self.overbought = 70
        self.oversold = 30

    def run(self, df):
        rsi_indicator = RSIIndicator(df["close"], 14)
        df["RSI"] = rsi_indicator.rsi()  # added a column with RSI osscilator

        res = []
        current_stock = 0
        lim = 100
        for i in range(len(df)):
            frame = df.iloc[i]
            d = {}
            d["timestamp"] = frame["timestamp"]
            #             print("fram rsi ",frame['RSI'])
            if frame["RSI"] <= self.oversold:
                d["actions"] = "buy"
                d["quantity"] = lim  # np.random.randint(0,lim,1)[0]
                current_stock += d["quantity"]

            elif frame["RSI"] >= self.overbought and current_stock > lim:
                d["actions"] = "sell"
                d["quantity"] = lim  # np.random.randint(,current_stock,1)[0]
                current_stock -= d["quantity"]

            else:
                continue
            res.append(d)

        return res


rs = RSIStrategy()
run = rs.run
