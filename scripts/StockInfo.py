import pandas as pd
class StockInfo:
    def __init__(self):
        self.df = None
        self.path = "./data/symbolMapping.csv"
        self.load() # start data load
        
    def __repr__(self):
        return "class to give stock mapping "
    
    def load(self):
        try:
            self.df= pd.read_csv(self.path)
        except:
            raise FileNotFoundError(self.path)
            
    def getLabelValueMap(self):
        temp = self.df.copy()
        temp.rename(columns={'name':'label','symbol':'value'},inplace=True)
        return temp.to_dict('records')
        