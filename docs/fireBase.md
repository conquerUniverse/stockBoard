# FireBase 
--

## DataBase Structure

DataBaseName = "StockData"

-- <Stock Short Name>
    |-- <Complete Name>
    |-- <Category>
    |--Prices
        |--Days
        |   |--<Date>
        |       |--High = <HighValue>
        |       |--Low = <LowValue>
        |       |--Open = <OpenValue>
        |       |--Close = <CloseValue>
        |       |--PE = <PE Ratio Value>
        |--Weekly
        |   |--<Date>
        |       |--High = <HighValue>
        |       |--Low = <LowValue>
        |       |--Open = <OpenValue>
        |       |--Close = <CloseValue>
        |       |--PE = <PE Ratio Value>

--