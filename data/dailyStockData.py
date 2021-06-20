import os
import yfinance as yf

col_map = {
    'Datetime':'timestamp',
    'Open':'open',
    'High':'high',
    'Low':'low',
    'Close':'close',
    'Volume':'volume'
}

def storeData(stockName, stockDataFrame, path):
    stockDataFrame = stockDataFrame.rename(columns=col_map)
    # stockDataFrame.index.rename('timestamp',inplace=True)
    stockDataFrame = stockDataFrame[['open','high','low','close','volume']]
    # print(stockDataFrame.head())
    # print(path + "\perMinuteWeeklyData")
    stockDataFrame.to_csv(os.path.join(path, "perMinuteWeeklyData",stockName+".csv"))

# print(os.getcwd())

def getStockData():
    nameFindpath = os.getcwd() + '\data\stockData\daily'
    savingPath = os.getcwd() + '\data\stockData'
    allStockSymbols = [ stockSymbol.split(".csv")[0] for stockSymbol in os.listdir(nameFindpath) ]


    for stockSymbol in allStockSymbols:
        exchangeSymbol = "NS" # NS
        symbol = stockSymbol.upper()+"."+exchangeSymbol
        stockData = yf.Ticker(symbol)
        perMinuteWeeklyStockData = stockData.history(period='5d', interval="1m")
        # print(perMinuteWeeklyStockData)
        if(len(perMinuteWeeklyStockData)):
            storeData(stockSymbol, perMinuteWeeklyStockData, savingPath)

getStockData()