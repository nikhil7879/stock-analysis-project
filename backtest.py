def backtest_strategy(data):
    # Make a copy so the original data is not changed by mistake
    backtest_data = data.copy()

    # Remove rows with missing values in important columns
    backtest_data = backtest_data.dropna(subset=["MA_3", "MA_5", "Daily_Return"])

    # Create trading position:
    # 1 = in the market, 0 = out of the market
    backtest_data["Position"] = (backtest_data["MA_3"] > backtest_data["MA_5"]).astype(int)

    # Shift by 1 day so we use yesterday's signal today
    backtest_data["Position"] = backtest_data["Position"].shift(1)

    # Fill the first empty value after shift with 0
    backtest_data["Position"] = backtest_data["Position"].fillna(0)

    # Calculate strategy daily return
    backtest_data["Strategy_Return"] = backtest_data["Position"] * backtest_data["Daily_Return"]

    # Calculate cumulative growth for stock and strategy
    backtest_data["Cumulative_Stock"] = (1 + backtest_data["Daily_Return"]).cumprod()
    backtest_data["Cumulative_Strategy"] = (1 + backtest_data["Strategy_Return"]).cumprod()

    return backtest_data
