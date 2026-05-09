import yfinance as yf

def load_stock_data(ticker, period="1y"):
    data = yf.download(ticker, period=period, auto_adjust=True)
    return data
