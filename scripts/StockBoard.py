import pandas as pd
import numpy as np
# import plotly.graph_objects as go
from dateutil.parser import parse
import pandasql as ps

class StockBoard:
    
    def __init__(self,data):
        """Contains all funciton of StockBoard"""
        self.data = data
        
    def getFilterdDate(self,dfName,date ):
        # date in string format
        df = self.data.getData(dfName)
        return df[df.Date <= parse(date)]

    def getInvestedValue(self):
        df = self.data.Invest
        return df[df.Description == 'add'].Amount.sum()

    def getTotalBrokerage(self):
        sd = self.data
        """ get total brokerage used including depository participant charges """
        df_sell = sd.Sell.BrokerageCost.sum()
        df_buy = sd.Buy.BrokerageCost.sum()
        df = sd.Invest
        df_invest = df[df.Description == 'DP Charges'].Amount.sum()
        return df_sell+df_buy+df_invest

    def getCurrBalance(self,):
        dfBuy, dfSell, dfInvest = self.data.Buy, self.data.Sell, self.data.Invest
        val =  sum(dfInvest.Amount)-(   sum(dfBuy.NumberOfStocks*dfBuy.BuyingPrice)+ \
                sum(dfBuy.BrokerageCost)+sum(dfSell.BrokerageCost) \

                -sum(dfSell.NumberOfStocks * dfSell.SellingPrice))
        return round(val,2)
    
    def getCurrHoldings(self,):
        dfBuy = self.data.Buy
        dfSell = self.data.Sell

        data = ps.sqldf("""

        select a.Name,a.nStocks-coalesce(b.nStocks,0) as current from

        (select Name,sum(NumberOfStocks) as nStocks,sum(BuyingPrice*NumberOfStocks) as Value
        from dfBuy group by Name 
        ) a
        left outer join 
        (select Name,sum(NumberOfStocks) as nStocks,sum(SellingPrice*NumberOfStocks) as Value
        from dfSell group by Name) b

        on a.Name = b.Name
        where a.nStocks > coalesce(b.nStocks,0)
        """)
        return data