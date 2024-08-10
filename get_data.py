import pandas as pd
import datetime as dt
import yfinance as yf
#

def download_data(tickers,start_date,end_date):
    """  download data from yahoo finance and save to a csv file given a list of tickers"""
    for ticker in tickers:
        df = yf.download(ticker, start=start_date, end=end_date, interval='1d')
        df.to_csv("{}.csv".format(ticker))
    return "done downloading data"

# test out the function

if __name__ == "__main__":
    tickers = ['QQQ', 'SPY', 'BTC-USD', 'ETH-USD', 'GC=F']
    start='2024-01-01'
    end='2024-08-03'
    download_data(tickers,start,end)