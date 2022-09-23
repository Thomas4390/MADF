import pandas as pd

from Class.RollingWindow import RollingDataSet


def transformPricesToYield(
        priceData: pd.DataFrame, yieldPeriod: int = 1
) -> pd.DataFrame:
    yieldData = priceData / priceData.shift(yieldPeriod) - 1
    return yieldData.iloc[yieldPeriod:, :]


def createRollingData(data: pd.DataFrame, window: int) -> RollingDataSet:
    # À chaque next: i += 1
    # on a comme retour le dataframe qui va de data.iloc[i*window : (i+1)*window, :]
    pass
