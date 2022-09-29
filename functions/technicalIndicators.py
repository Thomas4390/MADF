from typing import Callable, List, Any, Tuple
import talib

import numpy as np
import pandas as pd


# Les indicateurs retournés à chaque


def ADX(stockPrice: pd.Series) -> List[Any]:
    pass


def AROON(stockPrice: pd.Series, period: int = 25) -> List[Any]:
    aroonIndicators = {
        "up": [np.nan] * period,
        "down": [np.nan] * period,
        "diff": [np.nan] * period,
        "date": list(stockPrice.index[:period]),
    }
    for idx in range(stockPrice.shape[0] - period):
        currentPeriodStockPrice: pd.Series = stockPrice.iloc[idx : idx + period]
        aroonIndicators["date"].append(stockPrice.index[idx + period])
        if currentPeriodStockPrice.isnull().any():
            aroonIndicators["up"].append(np.nan)
            aroonIndicators["down"].append(np.nan)
            aroonIndicators["diff"].append(np.nan)
        else:
            aroonIndicators["up"].append(
                np.argmax(currentPeriodStockPrice) * 100 / period
            )
            aroonIndicators["down"].append(
                np.argmin(currentPeriodStockPrice) * 100 / period
            )
            aroonIndicators["diff"].append(
                aroonIndicators["up"][-1] - aroonIndicators["down"][-1]
            )
    return aroonIndicators["diff"]


def APO(
    close_price: pd.Series, fastperiod: int = 12, slowperiod: int = 26, matype: int = 0
) -> pd.Series:
    """

    :param close_price:
    :param fastperiod:
    :param slowperiod:
    :param matype:
    :return:
    """

    return talib.APO(
        close_price, fastperiod=fastperiod, slowperiod=slowperiod, matype=matype
    )


def MACD(
    close_price: pd.Series,
    fastperiod: int = 12,
    slowperiod: int = 26,
    signalperiod: int = 9,
    select: str = "macd",
) -> pd.Series:
    """

    :param close_price:
    :param fastperiod:
    :param slowperiod:
    :param signalperiod:
    :param select:
    :return:
    """

    macd, macdsignal, macdhist = talib.MACD(
        close_price,
        fastperiod=fastperiod,
        slowperiod=slowperiod,
        signalperiod=signalperiod,
    )
    if select == "macd":
        return macd

    if select == "macdsignal":
        return macdsignal


def MACDEXT(
    close_price: pd.Series,
    fastperiod: int = 12,
    fastmatype: int = 0,
    slowperiod: int = 26,
    slowmatype: int = 0,
    signalperiod: int = 9,
    signalmatype: int = 0,
    select: str = "macd",
) -> pd.Series:
    """

    :param close_price:
    :param fastperiod:
    :param fastmatype:
    :param slowperiod:
    :param slowmatype:
    :param signalperiod:
    :param signalmatype:
    :return:
    """

    macd, macdsignal, macdhist = talib.MACDEXT(
        close_price,
        fastperiod=fastperiod,
        fastmatype=fastmatype,
        slowperiod=slowperiod,
        slowmatype=slowmatype,
        signalperiod=signalperiod,
        signalmatype=signalmatype,
    )

    if select == "macd":
        return macd

    if select == "macdsignal":
        return macdsignal


# def MACDFIX(close_price: pd.Series, signal_period: int = 9, select: str = "macd") -> pd.Series:
#    """
#
#    :param close_price:
#    :param signal_period:
#    :param select:
#    :return:
#    """
#
#    macd, macdsignal, macdhist = talib.MACDFIX(close_price, signal_period=signal_period)
#
#    if select == "macd":
#        return macd
#
#    if select == "macdsignal":
#        return macdsignal


def CMO(close_price: pd.Series, time_period: int = 14):
    """
    Chande Momentum Oscillator
    :param close_price:
    :param time_period:
    :return:
    """

    return talib.CMO(close_price, time_period=time_period)


def MOM(close_price: pd.Series, timeperiod: int = 10) -> pd.Series:
    """

    :param close_price:
    :param timeperiod:
    :return:
    """

    return talib.MOM(close_price, timeperiod=timeperiod)


def RSI(close_price: pd.Series, timeperiod: int = 14) -> pd.Series:

    """

    :param close_price:
    :param timeperiod:
    :return:
    """
    return talib.RSI(close_price, timeperiod=timeperiod)


def TRIX(close_price: pd.Series, timeperiod: int = 30) -> pd.Series:

    """

    :param close_price:
    :param timeperiod:
    :return:
    """
    return talib.TRIX(close_price, timeperiod=timeperiod)


def STOCHRSI(
    close_price: pd.Series,
    timeperiod: int = 10,
    fastk_period: int = 5,
    fastd_period: int = 3,
    fastd_matype: int = 0,
    select: str = "fastk",
) -> pd.Series:

    """

    :param close_price:
    :param timeperiod:
    :param fastk_period:
    :param fastd_period:
    :param fastd_matype:
    :param select:
    :return:
    """

    fastk, fastd = talib.STOCHRSI(
        close_price,
        timeperiod=timeperiod,
        fastk_period=fastk_period,
        fastd_period=fastd_period,
        fastd_matype=fastd_matype,
    )

    if select == "fastk":
        return fastk

    if select == "fastd":
        return fastd


def PPO(
    close_price: pd.Series, fastperiod: int = 12, slowperiod: int = 26, matype: int = 0
) -> pd.Series:
    """

    :param close_price:
    :param fastperiod:
    :param slowperiod:
    :param matype:
    :return:
    """

    return talib.PPO(
        close_price, fastperiod=fastperiod, slowperiod=slowperiod, matype=matype
    )


def addNewIndicator(
    indicatorFunction: Callable, indicatorName: str, priceDataFrame: pd.DataFrame
) -> pd.DataFrame:
    indicatorDataFrame = priceDataFrame.apply(indicatorFunction, axis=0)
    name = indicatorName
    indicatorDataFrame.columns = map(
        lambda x: name + " | " + x, indicatorDataFrame.columns
    )
    return indicatorDataFrame
