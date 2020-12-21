# FireBase 
---

## DataBase Structure

DataBaseName = "StockData"
```
 <Stock Short Name>
    |-- Name = <Complete Name>
    |-- Category = <Category>
    |--Prices
        |--Days
        |   |--date = <Date> 
        |       |--High = <HighValue>
        |       |--Low = <LowValue>
        |       |--Open = <OpenValue>
        |       |--Close = <CloseValue>
        |       |--PE = <PE Ratio Value>
        |--Weekly
        |   |--date = <Date>
        |       |--High = <HighValue>
        |       |--Low = <LowValue>
        |       |--Open = <OpenValue>
        |       |--Close = <CloseValue>
        |       |--PE = <PE Ratio Value>

```