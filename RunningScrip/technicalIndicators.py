import matplotlib.pyplot as plt
import pandas as pd
from RunningScrip.newVariableForPairTrading import createModifiedVariableForPairTrading
from functions.technicalIndicators import *
from typing import Callable, Dict, List, Tuple

indicators = {
    "AROON": AROON,
    #"APO": APO,
    "MACD": MACD
    #"MACDEXT": MACDEXT,
    #"MOM": MOM,
    #"PPO": PPO,
    #"RSI": RSI,
    #"STOCHRSI": STOCHRSI,
    #"TRIX": TRIX
}

def getData(
    rollingWindow: int = 60,
    numberOfPairsToTrade: int = 2,
    method: str = "alphaFactor",
    indicators: Dict[str, Callable] = {"MACD": MACD}
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
    indicatorsDataFrame = pd.DataFrame(index=newVariableDataFrame.index)

    # Ajout des indicateurs techniques dans le dataframe pour indicateur.
    #TODO : Calculer les indicateurs dans une autre DataFrame.
    # Il est ensuite possible de concat les deux dataFrame en une seule étape.
    for key, value in indicators.items():
        indicatorsDataFrame = indicatorsDataFrame.join(
            addNewIndicator(value, key, newVariableDataFrame)
        )


    # indicatorsDataFrame = indicatorsDataFrame.join(MOM(newVariableDataFrame))
    # indicatorsDataFrame = indicatorsDataFrame.join(addNewIndicator(ADX, 'ADX', newVariableDataFrame))
    # indicatorsDataFrame = indicatorsDataFrame.join(addNewIndicator(MACD, 'MACD', newVariableDataFrame))
    # indicatorsDataFrame = indicatorsDataFrame.join(addNewIndicator(RSI, 'RSI', newVariableDataFrame))
    # indicatorsDataFrame = indicatorsDataFrame.join(addNewIndicator(SMI, 'SMI', newVariableDataFrame))

    # for column in newVariableDataFrame.columns:
    #     plt.plot(np.log(1+newVariableDataFrame[column]), label=column)
    # plt.legend()
    #
    # # fig, ax = plt.subplots(2)
    # # for column in newVariableDataFrame.columns:
    # #     ax[0].plot(newVariableDataFrame[column], label=column)
    # # ax[0].legend()
    #
    # # for column in indicatorsDataFrame.columns:
    # #     ax[1].plot(indicatorsDataFrame[column], label=column)
    # # ax[1].plot(indicatorsDataFrame.iloc[:, 1], label=indicatorsDataFrame.columns[1])
    # # ax[1].legend()
    #
    # plt.show()
    return newVariableDataFrame, newVariableToTradeDataFrame, indicatorsDataFrame


newVariableDataFrame, newVariableToTradeDataFrame, indicatorsDataFrame = getData(indicators=indicators)

if __name__ == "__main__":
    getData(indicators=indicators)


