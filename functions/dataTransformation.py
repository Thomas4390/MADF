import numpy as np
import pandas as pd

from Class.RollingWindow import MyRollingWindow
from functions.importationTitres import get_sp_data
from collections.abc import Iterator
from typing import List


def transformPricesToYield(
        priceData: pd.DataFrame, yieldPeriod: int = 1
) -> pd.DataFrame:
    yieldData = priceData / priceData.shift(yieldPeriod) - 1
    return yieldData.iloc[yieldPeriod:, :]


def compute_correlation(df: pd.DataFrame, column: str = "Adj Close") -> pd.DataFrame:
    return df[column].corr()


def find_n_max_pairs(df_corr: pd.DataFrame, n_max: int = 10) -> List[List]:
    """
    Trouve les n_max paires avec le plus grand coefficient de corrélation
    sans prendre en compte la diagonale de 1.

    :param df_corr: matrice de corrélation
    :param n_max: nombre de paires maximums à renvoyer
    :return: List[List] : La liste de toutes les n plus grandes paires.
    On précise que même si elles ne sont pas triées par ordre décroissant
    dans la liste retourné, les n plus grandes paires sont bien présentes.
    """

    # On convertit la matrice de corrélation au format ndarray
    df_corr_np = df_corr.to_numpy()
    # On remplit la diagonale de 1
    df_corr_np = np.tril([1] * df_corr_np.shape[0], -1) * df_corr_np

    # Trouve les n plus grands indices dans l'array "flattened"

    # indices = np.unravel_index(df_corr_np.argmax(), df_corr_np.shape)
    # indices = np.argpartition(df_corr_np)[-n_max:]
    x, y = np.unravel_index(np.argsort(df_corr_np, axis=None), df_corr_np.shape)
    # indices = np.abs(df_corr_np).argpartition(n_max, axis=None) #[-n_max:]

    # Convertit les indices "flattened" en indices matriciels selon
    # le format de la matrice de corrélation
    # x, y = np.unravel_index(indices, df_corr_np.shape)
    # Retrouve les paires associés avec les coordonnées x et y.
    pairs_list = [[df_corr.index[a], df_corr.columns[b]] for a, b in zip(x[-n_max:], y[-n_max:])]
    return pairs_list


def create_variable_to_trade(
        df_close: pd.DataFrame, pairs_list: List[List], method: str = "diff"
) -> pd.DataFrame:
    """
    :param df_transform: pd.Dataframe. Contient la série des prix "Adj Close"
    au cours du temps.
    :param pairs_list: La liste des n plus grandes paires renvoyés par
    la fonction find_n_max_pairs
    :param method: str. Peut prendre la valeur "diff" par défaut pour faire
    la différence entre deux séries ou la valeur "div" pour faire la division.
    :return: df_transform: pd.DataFrame. Renvoie la DataFrame de la série
    transformé entre les paires de stocks.
    """
    df_transform = pd.DataFrame()

    if method == "diff":
        for i in range(len(pairs_list)):
            df_transform[f"{pairs_list[i][0]} - {pairs_list[i][1]}"] = (
                    df_close[pairs_list[i][0]] - df_close[pairs_list[i][1]]
            )

    elif method == "div":
        for i in range(len(pairs_list)):
            df_transform[f"{pairs_list[i][0]} / {pairs_list[i][1]}"] = (
                    df_close[pairs_list[i][0]] / df_close[pairs_list[i][1]]
            )

    else:
        print("Invalid Method. Please try 'diff' or 'div'.")

    return df_transform
