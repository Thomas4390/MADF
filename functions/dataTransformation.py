import numpy as np
import pandas as pd
from functions.importationTitres import get_sp_data
from collections.abc import Iterator



def transformPricesToYield(
        priceData: pd.DataFrame, yieldPeriod: int = 1
) -> pd.DataFrame:
    yieldData = priceData / priceData.shift(yieldPeriod) - 1
    return yieldData.iloc[yieldPeriod:, :]


def createRollingData(df: pd.DataFrame, window: int):
    # À chaque next: i += 1
    # on a comme retour le dataframe qui va de data.iloc[i*window : (i+1)*window, :]
    class MyRollingWindow(Iterator):

        def __init__(self, df, window, i: int = 0):
            self.df = df
            self.window = window
            self.i = i

        def __next__(self):
            if self.i == 0:
                return self.df.iloc[
                       self.i * self.window: (self.i + 1) * self.window]

            self.i += 1

            return self.df.iloc[
                   self.i * self.window: (self.i + 1) * self.window]

    return MyRollingWindow

def compute_correlation(df: pd.DataFrame, column: str = "Adj Close") -> pd.DataFrame:

    return df[column].corr()

def find_n_pairs(df_corr: np.ndarray, n_max:int = 10) -> List[List]:
    """
    Trouve les n_max paires avec le plus grand coefficient de corrélation
    sans prendre en compte la diagonale de 1.

    :param df_corr: matrice de corrélation
    :param n_max: nombre de paires maximums à renvoyer
    :return: List[List] : La liste de toutes les n plus grandes paires.
    """

    df_corr_np = df_corr.to_numpy()
    np.fill_diagonal(df_corr_np, 0)
    indices = (-df_corr_np).argpartition(n_max, axis=None)[:n_max]
    x, y = np.unravel_index(indices, df_corr_np.shape)
    pairs_list = [[df_corr.index[a], df_corr.columns[b]] for a, b in zip(x, y)]
    return pairs_list