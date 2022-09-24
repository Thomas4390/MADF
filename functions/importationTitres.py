from typing import List
import yfinance as yf

import pandas as pd


def importDataFromYahoo(
    tickers: List[str], timing: str = "Adj Close", interval: str = "1d"
) -> pd.DataFrame:
    priceData: pd.DataFrame = yf.download(tickers,
                                          interval=interval,
                                          period="max")[timing]
    priceData.replace(0, pd.NA, inplace=True)
    return priceData


def get_sp_data(start: str = "2008-01-01", end: str = None) -> pd.DataFrame:
    # Get the current SP components, and get a tickers list
    sp_assets = pd.read_html(
        "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    )[0]
    assets = sp_assets["Symbol"].str.replace(".", "-").tolist()
    # Download historical data to a multi-index DataFrame
    try:
        data = yf.download(assets, start=start, end=end)
        # HDF5 is a good format for storing large amounts of data
        filename = "sp_500_data.hdf"
        data.to_hdf(f"data/{filename}", key="df")
        print(f"Data saved at {filename}")
    except ValueError:
        print("Failed download, try again.")
        data = None
    return data
