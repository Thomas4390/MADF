import numpy as np
import pandas as pd

from functions.importationTitres import read_sp_data
from Class.RollingWindow import MyRollingWindow
from functions.importationTitres import download_sp_data
from collections.abc import Iterator
from typing import List


def transformPricesToYield(
    df_close: pd.DataFrame, yieldPeriod: int = 1
) -> pd.DataFrame:
    """

    :param df_close:
    :param yieldPeriod:
    :return:
    """
    yieldData = df_close / df_close.shift(yieldPeriod) - 1
    return yieldData.iloc[yieldPeriod:, :]


def compute_correlation(df: pd.DataFrame) -> pd.DataFrame:
    """

    :param df:
    :return:
    """
    return df.corr()


def find_n_max_pairs(df_corr: pd.DataFrame, n_max: int = 5) -> List[List]:
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
    # On remplit la diagonale de 0
    df_corr_np = np.tril([1] * df_corr_np.shape[0], -1) * df_corr_np


    x, y = np.unravel_index(np.argsort(df_corr_np, axis=None), df_corr_np.shape)

    pairs_list = [
        [df_corr.index[a], df_corr.columns[b]] for a, b in zip(x[-n_max:], y[-n_max:])
    ][::-1]

    return pairs_list


def create_variable_to_trade(
    df_close: pd.DataFrame, pairs_list: List[List], method: str = "norm"
) -> pd.DataFrame:
    """
    :param df_close:  pd.Dataframe. Contient la série des prix "Adj Close"
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
            df_transform[f"{pairs_list[i][0]}-{pairs_list[i][1]}"] = (
                df_close[pairs_list[i][0]] - df_close[pairs_list[i][1]]
            )

    elif method == "div":
        for i in range(len(pairs_list)):
            df_transform[f"{pairs_list[i][0]}-{pairs_list[i][1]}"] = (
                df_close[pairs_list[i][0]] / df_close[pairs_list[i][1]]
            )

    elif method == "norm":
        for i in range(len(pairs_list)):
            # alpha = np.array([np.nan] + list(df_close[pairs_list[i][0]] / df_close[pairs_list[i][1]])[:-1])
            lastPrice_0 = np.array([np.nan] + list(df_close[pairs_list[i][0]][:-1]))
            lastPrice_1 = np.array([np.nan] + list(df_close[pairs_list[i][1]][:-1]))

            df_transform[f"{pairs_list[i][0]}-{pairs_list[i][1]}"] = (
                (
                    df_close[pairs_list[i][0]] / lastPrice_0
                    - df_close[pairs_list[i][1]] / lastPrice_1
                )
                + 1
            ).cumprod(axis=0)
            df_transform.iloc[0, :] = np.nan

    else:
        print("Invalid Method. Please try 'diff', 'div' or 'norm'.")

    return df_transform
def stack_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    :param df: pd.DataFrame. DataFrame à transformer
    :return: df_stack: pd.DataFrame. DataFrame

    """
    df_stack = df.stack().reset_index()
    # Nom des colonnes
    df_stack.columns = ["Date", "Paire", "Prix"]
    # Grouper les données par nom de titre dans le multi index
    df_stack = df_stack.groupby("Paire").apply(lambda x: x.set_index(["Date"]))
    # Supprimer le multi index
    df_stack = df_stack.droplevel(0)

    return df_stack

