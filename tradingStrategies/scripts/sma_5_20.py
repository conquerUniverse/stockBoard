
def run(df):
    """sma report on df"""
    long = "smaLong"
    short = "smaShort"
    window_long = 50
    window_short = 10
    qty = 10
    currAmount = 0

    print("running sma ",window_short,window_long)
    
    state = ''

    df[long] = df["close"].rolling(window=window_short).mean()
    df[short] = df["close"].rolling(window=window_long).mean()
    res = []
    trans = 0
    for i in range(len(df)):
        d = {}
        d["actions"] = ''
        d['quantity'] = 0
        # trans+=1

        # if trans < 10:
        #     res.append(d)
        #     continue

        if df[long].iloc[i] >= df[short].iloc[i] and state != 'buy':
            d["actions"] = 'buy'
            d["quantity"] = qty
            currAmount += qty
            state = 'buy'
            trans = 0
        elif df[long].iloc[i] < df[short].iloc[i] and state != 'sell':
            d["actions"] = 'sell'
            d["quantity"] = min(qty,currAmount)
            state = 'sell'
            currAmount -= min(qty,currAmount)
            trans = 0
            
        if d['quantity'] == 0:
            d['actions'] = ''
        res.append(d)
    return res
        