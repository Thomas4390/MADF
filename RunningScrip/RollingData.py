import matplotlib.pyplot as plt
import pandas as pd
from RunningScrip.newVariableForPairTrading import createModifiedVariableForPairTrading
from functions.technicalIndicators import *
from typing import Callable, Dict, List, Tuple

indicators = {
    "AROON": AROON,
    "AROON_UP": AROON_UP,
    "AROON_DOWN": AROON_DOWN,
    "MACD": MACD,
    "RSI": RSI,
    "STOCHRSI": STOCHRSI,
    "TRIX": TRIX,
    "PPO": PPO,
    "STC": STC,
    "KAMA": KAMA,
    "KST": KST,
    "DPO": DPO,
    "BOLLINGER": BOLLINGER,
    "ULCER": ULCER,
    "TSI": TSI,
    "EMA": EMA
}

def getData(
    rollingWindow: int = 60,
    numberOfPairsToTrade: int = 2,
    method: str = "norm",
    indicators: Dict[str, Callable] = {"MACD": MACD},
    save_to_pickle: bool = False
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """

    :param rollingWindow:
    :param numberOfPairsToTrade:
    :param method:
    :param indicators: Dictionnaire des indicateurs à fournir
    :return:
    """
    (
        newVariableDataFrame,
        newVariableToTradeDataFrame,
    ) = createModifiedVariableForPairTrading(
        rollingWindow=rollingWindow,
        numberOfPairsToTrade=numberOfPairsToTrade,
        method=method,
    )

    # Création du dataframe pour les indicateurs techniques
    df_indicators = AddingNewIndicators(newVariableDataFrame, indicators)

    if save_to_pickle:
        newVariableDataFrame.to_pickle(
            f"../data/newVariableDataFrame{rollingWindow}_{numberOfPairsToTrade}.pkl")
        newVariableToTradeDataFrame.to_pickle(
            f"../data/newVariableToTradeDataFrame{rollingWindow}_{numberOfPairsToTrade}.pkl")
        df_indicators.to_pickle(f"../data/indicatorsDataFrame{rollingWindow}_{numberOfPairsToTrade}.pkl")


    return newVariableDataFrame, newVariableToTradeDataFrame, df_indicators


