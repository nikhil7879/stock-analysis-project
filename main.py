import sys
import pandas as pd
import matplotlib.pyplot as plt

sys.path.append("/content/stock_project/src")

from data_loader import load_stock_data
from indicators import add_daily_return, add_moving_average_3, add_moving_average_5
from signals import get_trend_signal, get_action_signal
from backtest import backtest_strategy


def analyze_stock(ticker, period="1y", show_plots=False):
    data = load_stock_data(ticker, period=period)
    data.columns = data.columns.get_level_values(0)
    data = add_daily_return(data)
    data = add_moving_average_3(data)
    data = add_moving_average_5(data)

    data["Daily_Return_Percent"] = data["Daily_Return"] * 100

    last_row = data.iloc[-1]
    latest_date = str(data.index[-1].date())
    trend_signal = get_trend_signal(last_row)
    action_signal = get_action_signal(last_row)
    latest_close = round(last_row["Close"], 2)
    latest_daily_return_percent = round(last_row["Daily_Return_Percent"], 2)

    backtest_data = backtest_strategy(data)

    final_stock_value = backtest_data["Cumulative_Stock"].iloc[-1]
    final_strategy_value = backtest_data["Cumulative_Strategy"].iloc[-1]

    stock_return_percent = round((final_stock_value - 1) * 100, 2)
    strategy_return_percent = round((final_strategy_value - 1) * 100, 2)

    if show_plots:
        plt.figure(figsize=(12, 6))
        plt.plot(data.index, data["Close"], label="Close")
        plt.plot(data.index, data["MA_3"], label="MA_3")
        plt.plot(data.index, data["MA_5"], label="MA_5")
        plt.title(f"{ticker} Close Price with Moving Averages ({period})")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.legend()
        plt.show()

        plt.figure(figsize=(12, 6))
        plt.plot(backtest_data.index, backtest_data["Cumulative_Stock"], label="Buy and Hold")
        plt.plot(backtest_data.index, backtest_data["Cumulative_Strategy"], label="Strategy")
        plt.title(f"{ticker} Backtest Performance ({period})")
        plt.xlabel("Date")
        plt.ylabel("Growth of $1")
        plt.legend()
        plt.show()

    return {
        "Ticker": ticker,
        "Latest Date": latest_date,
        "Latest Close": latest_close,
        "Trend Signal": trend_signal,
        "Action Signal": action_signal,
        "Latest Daily Return %": latest_daily_return_percent,
        "Buy and Hold Return %": stock_return_percent,
        "Strategy Return %": strategy_return_percent
    }


def choose_winner(edge):
    if edge > 0:
        return "Strategy"
    elif edge < 0:
        return "Buy and Hold"
    else:
        return "Tie"


def create_summary_table(tickers, period="6mo"):
    results = []

    for ticker in tickers:
        row = analyze_stock(ticker, period=period, show_plots=False)
        results.append(row)

    summary_df = pd.DataFrame(results)

    summary_df["Strategy Edge %"] = (
        summary_df["Strategy Return %"] - summary_df["Buy and Hold Return %"]
    )

    summary_df["Winner"] = summary_df["Strategy Edge %"].apply(choose_winner)

    summary_df = summary_df.sort_values(by="Strategy Edge %", ascending=False)

    return summary_df


def save_strategy_edge_chart(summary_df, output_path):
    colors = ["green" if value > 0 else "red" if value < 0 else "gray"
              for value in summary_df["Strategy Edge %"]]

    plt.figure(figsize=(10, 6))
    bars = plt.bar(summary_df["Ticker"], summary_df["Strategy Edge %"], color=colors)

    plt.axhline(0, color="black", linewidth=1)
    plt.title("Strategy Edge by Ticker")
    plt.xlabel("Ticker")
    plt.ylabel("Strategy Edge %")

    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            f"{height:.2f}",
            ha="center",
            va="bottom" if height > 0 else "top"
        )

    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()


def main(tickers, period, csv_path, chart_path):
    summary_df = create_summary_table(tickers, period=period)

    summary_df.to_csv(csv_path, index=False)
    save_strategy_edge_chart(summary_df, chart_path)

    print("Final ranked summary table:")
    print(summary_df)
    print()
    print(f"CSV saved to: {csv_path}")
    print(f"Chart saved to: {chart_path}")
if __name__ == "__main__":
    tickers = ["META", "AMZN", "GOOGL"]
    period = "1y"
    csv_path = "/content/stock_project/tech_stock_summary.csv"
    chart_path = "/content/stock_project/tech_strategy_edge_chart.png"

    main(tickers, period, csv_path, chart_path)
