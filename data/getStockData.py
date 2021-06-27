import argparse
from datetime import datetime
import os, json,time
import yfinance as yf
from termcolor import colored, cprint
from concurrent.futures import ThreadPoolExecutor

# parse arguements
parser = argparse.ArgumentParser()
parser.add_argument("-S","--savepath",help="Location of path to update data",
    type=str,default=os.path.join('data','stockData','daily'))
parser.add_argument("-M","--meta",help="metadata file path",
    type=str,default=os.path.join('data','metadata.json'))
parser.add_argument("-D","--daily",help="get daily data ", 
    action="store_true")
parser.add_argument("-W","--weekly",help="get weekly data ", 
    action="store_true")
parser.add_argument("-V","--verbose",help="detailed logs", 
    action="store_true")

args = parser.parse_args()
print(args)
print(os.getcwd())


class MetaDataUpdates:
    def __init__(self,args):
        self.location = args.meta
        self.data = None

    def loadMetaData(self):
        with open(self.location,'r') as F:
            self.data = json.loads(F.read())
        self.daily_date = self.data['daily']['latest_date'] #datetime.strptime(self.data['daily']['latest_date'],'%Y-%m-%d')
        self.weekly_date = datetime.strptime(self.data['perMinuteWeeklyData']['latest_date'],"%Y-%m-%d %H:%M:%S")
    
    def writeMetaData(self):
        with open(self.location,'w') as F:
            F.write(json.dumps(self.data,indent=4))
        print("meta data written")

md = MetaDataUpdates(args)
md.loadMetaData()



col_map = {
    "Datetime":"timestamp",
    "Open": "open",
    "High": "high",
    "Low": "low",
    "Close": "close",
    "Volume": "volume",
}


def storeData(stockName, path=args.savepath):

    exchangeSymbol = "NS" 
    symbol = stockName.upper() + "." + exchangeSymbol
    stockData = yf.Ticker(symbol)
    # print(md.daily_date)
    if args.daily:
        dataframe = stockData.history(start=md.daily_date)
    else:
        dataframe = stockData.history(period="5d", interval="1m")
    
    try:
        stockDataFrame = dataframe.rename(columns=col_map)
        stockDataFrame = stockDataFrame[["open", "high", "low", "close", "volume"]]
        
        if len(stockDataFrame) > 0:
            stockDataFrame.to_csv(os.path.join(path,stockName + ".csv"),
            mode ='a',header=False)
            if args.verbose:
                cprint(f"SUCCESS : {stockName.upper()}",'green')
        else:
            cprint(f"SKIPPING : {stockName.upper()}",'red')
        
        
    except:
        if args.verbose:
            cprint(f"FAILED : {stockName.upper()}",'red')

    

def getExecutionTime(F,*args):
    startTime = time.time()
    print("#"*20)
    print("Number of Stocks data extracted ",F(*args))
    print("#"*20)
    endTime = time.time()
    cprint(f"total Execution time -> {round(endTime-startTime,3)}",
        'green')
    

def getStockData():
    nameFindpath = os.path.join(os.getcwd(),"data","stockData","daily")
    savingPath = args.savepath #os.path.join(os.getcwd(),args.savepath)
    allStockSymbols = [
        stockSymbol.split(".csv")[0] for stockSymbol in os.listdir(nameFindpath)
    ]
    if args.verbose:
        cprint(f"path {savingPath}",'yellow')

    with ThreadPoolExecutor(max_workers=16,thread_name_prefix='get_data_') as pool:
        results = pool.map(storeData, allStockSymbols)
    return len(allStockSymbols)

# start execution
getExecutionTime(getStockData)

if args.daily:
    md.data['daily']['latest_date'] = datetime.now().strftime('%Y-%m-%d')
elif args.weekly:
    md.data['perMinuteWeeklyData']['latest_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
md.writeMetaData()  
        
# Commands
# python data/getStockData.py --verbose -W -S data/stockData/perMinuteWeeklyData
# python data/getStockData.py --verbose -D -S data/stockData/daily 