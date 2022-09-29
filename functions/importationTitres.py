from typing import List
import yfinance as yf
import pandas as pd
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

def importDataFromYahoo(
    tickers: List[str], timing: str = "Adj Close", interval: str = "1d"
) -> pd.DataFrame:
    priceData: pd.DataFrame = yf.download(tickers, interval=interval, period="max")[
        timing
    ]
    priceData.replace(0, pd.NA, inplace=True)
    return priceData


def download_sp_data(start: str = "2005-01-01", end: str = "2022-08-01") -> pd.DataFrame:
    # Get the current SP components, and get a tickers list
    sp_assets = pd.read_html(
        "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    )[0]
    assets = sp_assets["Symbol"].str.replace(".", "-").tolist()
    # Download historical data to a multi-index DataFrame
    try:
        data = yf.download(assets, start=start, end=end)
        # HDF5 is a good format for storing large amounts of data
        filename = "sp_500_data.pkl"
        data.to_pickle(f"../data/{filename}")
        print(f"Data saved at {filename}")
    except ValueError:
        print("Failed download, try again.")
        data = None

def read_sp_data() -> pd.DataFrame:
    """

    :return:
    """
    df = pd.read_pickle("../data/sp_500_data.pkl")

    # df modifiée seulement pour faire des tests
    # On prend les 10 premières colonnes
    df_mod = df["Adj Close"][df["Adj Close"].columns[0:5]]

    return df_mod



if __name__ == "__main__":
    print(read_sp_data().head())
