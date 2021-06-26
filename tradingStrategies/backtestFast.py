import os
import pandas as pd
from multiprocessing import Process, Queue, Lock
import importlib


class BackTest:
    def __init__(self, loc, partition=4):
        self.loc = loc
        self.allStockList = os.listdir(self.loc)
        self.importSource = "tradingStrategies.scripts."
        self.stockVal = "close"
        self.scriptPath = "scripts"
        self.savePath = "tradingStrategies/results"
        self.partition = partition
        self.numberOfStocks = len(self.allStockList)

    def getPartition(
        self,
    ):
        total = self.numberOfStocks
        start = 0
        li = []
        for i in range(self.partition):
            end = (i + 1) * total // self.partition
            li.append((start, end))
            start = end
        return li

    def parseAction(self, a):
        a = a.lower()
        if a in ["buy", "sell"]:
            return a
        return ""

    def getTradeSummary(self, df):
        totalBuy = 0
        totalSell = 0
        totalInvestment = 0
        totalNetWorth = 0
        NumberOfTrades = 0
        stocksInHand = 0  # shorting is not allowed

        # assert len(df) == len(trades),"len of trade should be equal to stock result"
        L = len(df)

        for i in range(L):
            # trade = trades[i]
            stock = df.iloc[i]
            trade = df[["actions", "quantity"]].iloc[i].to_dict()

            action = self.parseAction(trade["actions"])
            qty = int(0 if trade["quantity"] == "" else trade["quantity"])

            if action == "buy":
                totalBuy += qty
                totalInvestment += qty * stock[self.stockVal]
                stocksInHand += qty

            if action == "sell":

                totalSell += qty
                totalNetWorth += qty * stock[self.stockVal]
                assert stocksInHand >= qty, "trying to sell more than you have"
                stocksInHand -= qty

            if action in ["buy", "sell"]:
                NumberOfTrades += 1

        ans = {}
        ans["totalInvestment"] = totalInvestment
        ans["totalNetWorth"] = totalNetWorth
        ans["NumberOfTrades"] = NumberOfTrades
        ans["totalBuy"] = totalBuy
        ans["totalSell"] = totalSell
        ans["currentStocksInHandValue"] = 0
        ans["stocksInHand"] = stocksInHand
        return ans

    def getScriptsName(self):
        names = [
            i[:-3]
            for i in os.listdir(self.scriptPath)
            if i[-3:] == ".py" and i != "__init__.py"
        ]
        return names

    def backtestMultiprocessing(self, func, stocksList, Q=None):
        scriptFunction = func
        fin_ans = []
        for i in stocksList:
            df = pd.read_csv(os.path.join(self.loc, i))
            trades = pd.DataFrame(scriptFunction(df))
            res = {}
            try:
                trades = pd.merge(df, trades, how="inner", on="timestamp")

            except:
                trades = pd.DataFrame()
            res = self.getTradeSummary(trades)
            res["name"] = i.split(".")[0]
            res["stockGrowth"] = (
                df.iloc[-1][self.stockVal] - df.iloc[0][self.stockVal]
            ) / df.iloc[0][self.stockVal]

            if res["stocksInHand"] > 0:
                res["currentStocksInHandValue"] = (
                    df.iloc[-1][self.stockVal] * res["stocksInHand"]
                )
            try:
                res["profitPercent"] = (
                    res["totalNetWorth"]
                    + res["currentStocksInHandValue"]
                    - res["totalInvestment"]
                ) / res["totalInvestment"]
            except:
                res["profitPercent"] = 0

            fin_ans.append(res)

        df = pd.DataFrame(fin_ans)
        Q.put(df)
        Q.put("done")

    def runMultiprocessing(self, scriptName, saveFile=False):
        Q = Queue()
        L = Lock()
        task = []
        instances = self.partition
        module = importlib.import_module(self.importSource + scriptName)
        scriptFunction = module.run
        print("function imported ")
        partitionList = self.getPartition()
        stockList = self.allStockList

        for i in range(instances):
            tempList = stockList[partitionList[i][0] : partitionList[i][1]]
            task.append(
                Process(
                    target=self.backtestMultiprocessing,
                    args=(scriptFunction, tempList, Q),
                )
            )
            task[i].start()
        print("Instances started")
        for i in range(instances):
            task[i].join()

        counter = 0
        df = None
        while Q and counter < instances:
            val = Q.get()
            if type(val) == type("") and val == "done":
                print("done received")
                counter += 1
            else:
                if df is None:
                    df = val
                else:
                    df = df.append(val)
        if saveFile:
            df.to_csv(os.path.join(self.savePath, scriptName + ".csv"), index=False)
        else:
            return df
