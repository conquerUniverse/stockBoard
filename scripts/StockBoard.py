import pandas as pd
import numpy as np
# import plotly.graph_objects as go
from dateutil.parser import parse
import pandasql as ps

class StockBoard:
    
    def __init__(self,data):
        """Contains all funciton of StockBoard"""
        self.data = data
        self.portfolioValue = 0
        self.investedValue = None
        self.currentBalance = None
        self.totalBrokerage = None
        # initial call functions
        self.getInvestedValue()
        self.getTotalBrokerage()
        self.getCurrBalance()
        # get profit value
        self.getPortfolioAmount()
        # self.getProfitValue()
        
    def getFilterdDate(self,dfName,date ):
        # date in string format
        df = self.data.getData(dfName)
        return df[df.Date <= parse(date)]
    
    def getBuyValue(self,stockName,count_val):
        df = self.data.Buy
        df = df[df.Name == stockName].sort_values('Date',ascending=False)
        val = 0
        for i in range(len(df)):
            c = min(count_val,df.iloc[i].NumberOfStocks)
            val += df.iloc[i].BuyingPrice*c
            count_val -= c
            if count_val <= 0:
                break
        return val
    
    def getPortfolioAmount(self,):
        ch = self.getCurrHoldings()
        portfolioValue = 0
        for i in range(len(ch)):
            name = ch.iloc[i]['Name']
            count_val = ch.iloc[i]['current']
            portfolioValue += self.getBuyValue(name,count_val)
        self.portfolioValue = portfolioValue
        return self.portfolioValue

    def getInvestedValue(self):
        if self.investedValue is not None:
            return self.investedValue
        df = self.data.Invest
        self.investedValue = df[df.Description == 'add'].Amount.sum()
        return self.investedValue 

    def getTotalBrokerage(self):
        if self.totalBrokerage is not None:
            return self.totalBrokerage
        sd = self.data
        """ get total brokerage used including depository participant charges """
        df_sell = sd.Sell.BrokerageCost.sum()
        df_buy = sd.Buy.BrokerageCost.sum()
        df = sd.Invest
        df_invest_dp = df[df.Description == 'DP Charges'].Amount.sum()
        df_invest_other = df[df.Description == 'other'].Amount.sum()
        self.totalBrokerage = df_sell+df_buy+abs(df_invest_dp +df_invest_other)
        return self.totalBrokerage

    def getCurrBalance(self,):
        if self.currentBalance is not None:
            return self.currentBalance
        dfBuy, dfSell, dfInvest = self.data.Buy, self.data.Sell, self.data.Invest
        val =  sum(dfInvest[dfInvest.Description != 'Dividend'].Amount)-(   sum(dfBuy.NumberOfStocks*dfBuy.BuyingPrice)+ \
                sum(dfBuy.BrokerageCost)+sum(dfSell.BrokerageCost) \

                -sum(dfSell.NumberOfStocks * dfSell.SellingPrice))

        self.currentBalance = round(val,2)
        return self.currentBalance
    
    def getProfitValue(self):
        """get profit value"""
        return round(self.investedValue - self.currentBalance - self.portfolioValue,2)
        
    
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