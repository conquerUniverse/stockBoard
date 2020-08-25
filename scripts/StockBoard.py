import pandas as pd
import numpy as np
# import plotly.graph_objects as go
from dateutil.parser import parse


class StockBoard:
    
    def __init__(self,data):
        """Contains all funciton of StockBoard"""
        self.data = data
        
    def getFilterdDate(self,dfName,date ):
        # date in string format
        df = self.data.getData(dfName)
        return df[df.Date <= parse(date)]

    def getCurrBalance(self,):
        dfBuy, dfSell, dfInvest = self.data.Buy, self.data.Sell, self.data.Invest
        val =  sum(dfInvest.Amount)-(   sum(dfBuy.NumberOfStocks*dfBuy.BuyingPrice)+ \
                sum(dfBuy.BrokerageCost)+sum(dfSell.BrokerageCost) \

                -sum(dfSell.NumberOfStocks * dfSell.SellingPrice))
        return round(val,2)