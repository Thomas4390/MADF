# Import the necessary modules
import pandas as pd
import yfinance as yf


def get_sp_data(start: str = "2008-01-01", end: str = None) -> pd.DataFrame:
    # Get the current SP components, and get a tickers list
    sp_assets = pd.read_html(
        "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    )[0]
    assets = sp_assets["Symbol"].str.replace(".", "-").tolist()
    # Download historical data to a multi-index DataFrame
    try:
        data = yf.download(assets, start=start, end=end)
        filename = "sp_500_data.pkl"
        data.to_pickle(f"data/{filename}")
        print(f"Data saved at {filename}")
    except ValueError:
        print("Failed download, try again.")
        data = None
    return data


if __name__ == "__main__":
    sp_data = get_sp_data()
