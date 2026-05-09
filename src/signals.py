def get_trend_signal(last_row):
    if last_row["MA_3"] > last_row["MA_5"]:
        return "Uptrend"
    elif last_row["MA_3"] < last_row["MA_5"]:
        return "Downtrend"
    else:
        return "Neutral"

def get_action_signal(last_row):
    if last_row["MA_3"] > last_row["MA_5"] and last_row["Daily_Return"] > 0:
        return "Buy"
    elif last_row["MA_3"] < last_row["MA_5"] and last_row["Daily_Return"] < 0:
        return "Sell"
    else:
        return "Hold"
