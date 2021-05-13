
def run(df):
    """sma report on df"""
    long = "smaLong"
    short = "smaShort"
    window_long = 20
    window_short = 5
    qty = 10
    currAmount = 0

    print("running sma ",window_short,window_long)
    
    state = ''

    df[long] = df["close"].rolling(window=window_short).mean()
    df[short] = df["close"].rolling(window=window_long).mean()
    res = []
    for i in range(len(df)):
        d = {}
        d["actions"] = ''
        d['quantity'] = 0
        if df[long].iloc[i] >= df[short].iloc[i] and state != 'buy':
            d["actions"] = 'buy'
            d["quantity"] = qty
            currAmount += qty
            state = 'buy'
        elif df[long].iloc[i] < df[short].iloc[i] and state != 'sell':
            d["actions"] = 'sell'
            d["quantity"] = min(qty,currAmount)
            state = 'sell'
            currAmount -= min(qty,currAmount)
            
        if d['quantity'] == 0:
            d['actions'] = ''
        res.append(d)
    return res
        