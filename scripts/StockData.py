import os
import pandas as pd
from datetime import datetime
import pytest


class StockData:
    def __init__(self, username="", location="profiles/"):
        self.Buy = None
        self.Sell = None
        self.Invest = None
        self.username = username
        self.location = os.path.join(location, username)
        assert os.path.isdir(self.location) == True, (
            self.location + " path not found \n curr path" + str(os.curdir)
        )
        self.isDataLoaded = False
        self.active_data = "buy"

    def load(
        self,
    ):
        """Load the values form ./profiles/<username> folder"""
        self.Buy = self.loadData("dfBuy.csv")
        self.Sell = self.loadData("dfSell.csv")
        self.Invest = self.loadData("dfInvest.csv")
        self.isDataLoaded = True
        # print("Files Successfully loaded")

    def getData(self, category=None):
        assert self.isDataLoaded, "Data is not loaded"
        if category is not None:
            self.active_data = self.parseCategory(category)
        dic = {"buy": self.Buy, "sell": self.Sell, "invest": self.Invest}
        return dic[self.active_data].sort_values(by="Date", ascending=False)

    def appendData_(self, category, new_df):
        assert self.isDataLoaded, "Data is not loaded"

        category = self.parseCategory(category)
        if category == "buy":
            self.Buy = self.Buy.append(new_df, ignore_index=True)
        elif category == "sell":
            self.Sell = self.Sell.append(new_df, ignore_index=True)
        elif category == "invest":
            self.Invest = self.Invest.append(new_df, ignore_index=True)
        else:
            raise "You should never be  here"

    def loadData(self, s):
        loc = os.path.join(self.location, s)
        assert os.path.isfile(loc) == True, f"{loc} file not found "
        return pd.read_csv(loc)

    def parseCategory(self, category):
        """Parse the category in correct format [standard]"""
        c = category.lower()
        assert c in ["sell", "buy", "invest"], "cannot find the correct category"
        return c

    def getDataStructure(self, category):
        # data Structure
        category = self.parseCategory(category)
        mapping = {
            "sell": {
                "Name": "",
                "NumberOfStocks": "",
                "SellingPrice": 0,
                "Date": datetime.now(),
                "TotalCost": 0,
                "ExtraCharges": 0,
            },
            "buy": {
                "Name": "",
                "NumberOfStocks": "",
                "BuyingPrice": 0,
                "Date": datetime.now(),
                "TotalCost": 0,
                "ExtraCharges": 0,
            },
            "invest": {
                "Amount": 0,
                "Date": datetime.now(),
                "Description": "add",
            },
        }
        return mapping[category]

    def checkStructureMapping(self, orig, given):
        for i in orig:
            assert i in given, f"structure mismatch {i} not found"

    def preprocessData(self, data, category="buy"):
        data = data.fillna(0)
        if category == "invest":
            return data
        data["BrokerageCost"] = 0
        if category == "buy":
            data.BrokerageCost = abs(
                data.TotalCost - data.NumberOfStocks * data.BuyingPrice
            )
        else:
            data.BrokerageCost = abs(
                -data.TotalCost + data.NumberOfStocks * data.SellingPrice
            )
        data.BrokerageCost += data.ExtraCharges

        return data.round(3)

    def addData(self, category, **kwargs):
        category = self.parseCategory(category)
        print(category)
        structure = self.getDataStructure(category)

        self.checkStructureMapping(structure, kwargs)
        new_df = pd.DataFrame(list(kwargs.values()), kwargs.keys()).T
        new_df = self.preprocessData(new_df, category)  # making right Format

        self.appendData_(category, new_df)

    def updateData(self, category, loc=None):
        """Actual update data and write in Disc"""
        loc = self.location if loc == None else loc

        category = self.parseCategory(category)
        mapping = {"sell": "dfSell.csv", "buy": "dfBuy.csv", "invest": "dfInvest.csv"}
        name = mapping[category]
        self.getData(category).to_csv(os.path.join(loc, name), index=False)

        print(f"{category} updated in {loc} sucessfully")
