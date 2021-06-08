import os
import pandas as pd
import importlib

class BackTest:
    def __init__(self,loc):
        self.loc = loc
        self.allStockList = os.listdir(self.loc)
        # print("stock list",self.allStockList)
        self.stockVal = 'close'
        self.scriptPath = "scripts"
        self.savePath = "results"
        self.importSource = 'tradingStrategies.scripts.'
        
    def parseAction(self,a):
        a = a.lower()
        if a in ['buy','sell']:
            return a
        return ''
    
    def getTradeSummary(self,df):
        totalBuy = 0
        totalSell = 0
        totalInvestment = 0
        totalNetWorth = 0
        NumberOfTrades = 0
        stocksInHand = 0 # shorting is not allowed
        
        # assert len(df) == len(trades),"len of trade should be equal to stock result"
        L = len(df)

        
        for i in range(L):
            # trade = trades[i]
            stock = df.iloc[i]
            trade = df[['actions','quantity']].iloc[i].to_dict()
            
            action = self.parseAction(trade['actions'])
            qty  = int(0 if trade['quantity'] == '' else trade['quantity'])
            
            if action == 'buy':
                totalBuy += qty
                totalInvestment += qty*stock[self.stockVal]
                stocksInHand += qty
                
            if action == 'sell':
                
                totalSell += qty  
                totalNetWorth += qty*stock[self.stockVal]
                assert stocksInHand >= qty,"trying to sell more than you have"
                stocksInHand -= qty
                
            if action in ['buy','sell']:
                NumberOfTrades += 1
        
        ans = {}
        ans["totalInvestment"] = totalInvestment
        ans["totalNetWorth"] = totalNetWorth
        ans["NumberOfTrades"] = NumberOfTrades
        ans["totalBuy"] = totalBuy
        ans["totalSell"] = totalSell
        ans["currentStocksInHandValue"] = 0
        ans['stocksInHand']  = stocksInHand
        return ans
        
    def getScriptsName(self):
        names = [i[:-3] for i in os.listdir(self.scriptPath) if i[-3:] == '.py' and i != '__init__.py']
        return names
    
    def backtest(self,scriptName,df):
        """scriptFunciton import and pass it 
        stocksList if empty will pick all the stocks else only the provided ones"""
        if type(scriptName) == type(''):
            # module = importlib.import_module(self.importSource)
            module = importlib.import_module(self.importSource+scriptName)
            scriptFunction = module.run
        else:
            scriptFunction = scriptName # funtion is provided in input directly
        trades = pd.DataFrame(scriptFunction(df))
        # print(trades)
        # print("col name in bac1111kgtets",trades.columns)
        trades = pd.merge(df,trades,how='inner',on='timestamp')

        res = self.getTradeSummary(trades)

        res["stockGrowth"] = (df.iloc[-1][self.stockVal] - df.iloc[0][self.stockVal])/df.iloc[0][self.stockVal]

        if res['stocksInHand'] > 0:
            res["currentStocksInHandValue"] = df.iloc[-1][self.stockVal]*res['stocksInHand']
        try:
            res["profitPercent"] = (res["totalNetWorth"]+res["currentStocksInHandValue"]
                              -res["totalInvestment"])/res["totalInvestment"]
        except:
            res["profitPercent"] = 0

        return res
