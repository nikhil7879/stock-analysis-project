def add_daily_return(data):
    data["Daily_Return"] = data["Close"].pct_change()
    return data

def add_moving_average_3(data):
    data["MA_3"] = data["Close"].rolling(window=3).mean()
    return data

def add_moving_average_5(data):
    data["MA_5"] = data["Close"].rolling(window=5).mean()
    return data
