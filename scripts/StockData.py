
import os
import pandas as pd
from datetime import datetime
import pytest
class StockData:
    def __init__(self,username = '', location = "profiles/"):
        self.Buy = None
        self.Sell = None
        self.Invest = None
        
        self.location = os.path.join(location,username)
        assert os.path.isdir(self.location) == True, self.location+" path not found"
        self.isDataLoaded = False
        
    
    def load(self,):
        """ Load the values form ./profiles/<username> folder"""
        self.Buy = self.loadData('dfBuy.csv')
        self.Sell = self.loadData('dfSell.csv')
        self.Invest = self.loadData('dfInvest.csv')
        self.isDataLoaded = True
        # print("Files Successfully loaded")
    
    def getData(self,category):
        assert self.isDataLoaded,"Data is not loaded"

        category = self.parseCategory(category)
        dic = {'buy':self.Buy, 'sell':self.Sell, 'invest':self.Invest}
        return dic[category]
        
    def loadData(self,s):
        loc = os.path.join(self.location,s)
        assert os.path.isfile(loc) == True,f"{loc} file not found "
        return pd.read_csv(loc)

    def parseCategory(self,category):
        """ Parse the category in correct format [standard]"""
        c = category.lower()
        assert c in ['sell','buy','invest'],'cannot find the correct category'
        return c

    def getDataStructure(self,category):
        # data Structure
        category = self.parseCategory(category)
        mapping = {
            'sell':{
                "Name":'',
                "NumberOfStocks":'',
                "SellingPrice":0,
                "Date":datetime.now(),
                "TotalCost":0,
                "ExtraCharges":0,
                },
            'buy':{
                "Name":'',
                "NumberOfStocks":'',
                "BuyingPrice":0,
                "Date":datetime.now(),
                "TotalCost":0,
                "ExtraCharges":0,
                },
            'invest':{
                "Amount":0,
                "Date":datetime.now(),
                "Description":'add',
                }
        }
        return mapping[category]
        
        
    def checkStructureMapping(self,orig,given):
        for i in orig:
            assert i in given, f"structure mismatch {i} not found"


    def addData(self,category,**kwargs):
        category = self.parseCategory(category)
        print(category)
        structure = self.getDataStructure(category)

        self.checkStructureMapping(structure,kwargs)
        df = self.getData(category)
        new_df = pd.DataFrame(list(kwargs.values()),kwargs.keys()).T
        df = df.append(new_df,ignore_index = True)

        # df updated
        print(df)
        
        
    def updateData(self,category,loc=None):
        loc =  self.location if loc == None else loc 

        category = self.parseCategory(category)
        mapping = {"sell":"dfSell.csv",
                    "buy":"dfBuy.csv",
                    "invest":"dfInvest.csv"
                    }
        name = mapping[category]

        loc = os.path.join(loc,name)

        print(f"{category} updated in {loc} sucessfully")

        