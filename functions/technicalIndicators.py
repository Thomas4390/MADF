from typing import Callable, List, Any

import numpy as np
import pandas as pd


# Les indicateurs retournés à chaque

def ADX(stockPrice: pd.Series) -> List[Any]:
    pass


def AROON(stockPrice: pd.Series, period: int = 25) -> List[Any]:
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


def MACD(stockPrice: pd.Series) -> List[Any]:
    pass


def RSI(stockPrice: pd.Series) -> List[Any]:
    pass


def SMI(stockPrice: pd.Series) -> List[Any]:
    pass


def addNewIndicator(indicatorFunction: Callable, indicatorName: str, priceDataFrame: pd.DataFrame) -> pd.DataFrame:
    indicatorDataFrame = priceDataFrame.apply(indicatorFunction, axis=0)
    name = indicatorName
    indicatorDataFrame.columns = map(lambda x: name + '-' + x, indicatorDataFrame.columns)
    return indicatorDataFrame
