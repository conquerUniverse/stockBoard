
import os
import pandas as pd
class StockData:
    def __init__(self,):
        self.Buy = None
        self.Sell = None
        self.Invest = None
        try:
            assert os.path.isdir('data') == True
        except:
            print("./data folder not found ")
            
        self.location = './data/'
    
    def load(self,):
        """ Load the values form ./data folder"""
        self.Buy = self.loadData('dfBuy.csv')
        self.Sell = self.loadData('dfSell.csv')
        self.Invest = self.loadData('dfInvest.csv')
        print("Files Successfully loaded")
    
    def getData(self,s):
        dic = {'buy':self.Buy, 'sell':self.Sell, 'invest':self.Invest}
        return dic[s.lower()]
        
    def loadData(self,s):
        try:
            assert os.path.isfile(self.location+s) == True
        except:
            print(f"{self.location+s} file not found ")
        return pd.read_csv(self.location+s)

        