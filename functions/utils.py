from typing import List
import yfinance as yf

import pandas as pd


def transformPricesToYield(priceData: pd.DataFrame, yieldPeriod: int = 1) -> pd.DataFrame:
    yieldData = priceData / priceData.shift(yieldPeriod) - 1
    return yieldData.iloc[yieldPeriod:, :]


def importDataFromYahoo(tickers: List[str], timing: str = 'Adj Close', interval: str = '1d') -> pd.DataFrame:
    priceData: pd.DataFrame = yf.download(tickers, interval=interval, period='max')[timing]
    priceData.replace(0, pd.NA, inplace=True)
    return priceData

