from typing import Callable, List, Any, Tuple
import talib

import numpy as np
import pandas as pd


# Les indicateurs retournés à chaque

def ADX(stockPrice: pd.Series) -> List[Any]:
    pass


def aroon(stockPrice: pd.Series, period: int = 25) -> List[Any]:
    aroonIndicators = {'up': [np.nan] * period,
                       'down': [np.nan] * period,
                       'diff': [np.nan] * period,
                       'date': list(stockPrice.index[:period])}
    for idx in range(stockPrice.shape[0] - period):
        currentPeriodStockPrice: pd.Series = stockPrice.iloc[idx:idx + period]
        aroonIndicators['date'].append(stockPrice.index[idx + period])
        if currentPeriodStockPrice.isnull().any():
            aroonIndicators['up'].append(np.nan)
            aroonIndicators['down'].append(np.nan)
            aroonIndicators['diff'].append(np.nan)
        else:
            aroonIndicators['up'].append(np.argmax(currentPeriodStockPrice) * 100 / period)
            aroonIndicators['down'].append(np.argmin(currentPeriodStockPrice) * 100 / period)
            aroonIndicators['diff'].append(aroonIndicators['up'][-1] - aroonIndicators['down'][-1])
    return aroonIndicators['diff']


def MACD(close: pd.Series,
         fastperiod: int = 12,
         slowperiod: int = 26,
         signalperiod: int = 9) -> Tuple[pd.Series, pd.Series]:

    macd, macdsignal, macdhist = talib.MACD(close=close,
                                      fastperiod=fastperiod,
                                      slowperiod=slowperiod,
                                      signalperiod=signalperiod)

    return macd, macdsignal

def MOM(close: pd.Series, timeperiod: int = 10) -> pd.Series:

    momentum = talib.MOM(close=close,
                         timeperiod=timeperiod)

    return momentum


def RSI(close: pd.Series, timeperiod: int = 10) -> pd.Series:
    rsi = talib.RSI(close=close, timeperiod=timeperiod)

    return rsi


def STOCHRSI(close: pd.Series,
        timeperiod: int = 10,
        fastk_period: int = 5,
        fastd_period: int = 3,
        fastd_matype: int = 0) -> Tuple[pd.Series, pd.Series]:

    fastk, fastd = STOCHRSI(close=close,
                            timeperiod=timeperiod,
                            fastk_period=fastk_period,
                            fastd_period=fastd_period,
                            fastd_matype=fastd_matype)

    return fastk, fastd


def addNewIndicator(indicatorFunction: Callable, indicatorName: str, priceDataFrame: pd.DataFrame) -> pd.DataFrame:
    indicatorDataFrame = priceDataFrame.apply(indicatorFunction, axis=0)
    name = indicatorName
    indicatorDataFrame.columns = map(lambda x: name + '-' + x, indicatorDataFrame.columns)
    return indicatorDataFrame
