# General Documentation 

# assets
- Contains extra file needed for the StocBoard App

# Data
- Cumulative data of the Stocks

# Profiles
- it has its own readme

# Scripts
-
## StockData (Class Name)
    - load(location ="../data/")  
        - Load the Data from the given location

    - getData(category) 
        - buy,sell,invest
        - return the pandas dataframe of the category

    - loadData(s)
        - internal use function for load
        - load the file name specified 
    - addData(category,**kwargs)
        - dictionary arg all values of specified category
        - check fullfillment of values
        - save the data in ram Dataframe
    
    - updateData(categor,loc)
        - update the data in the disk


StockBoard