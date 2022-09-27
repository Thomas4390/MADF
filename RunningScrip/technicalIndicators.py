import pandas as pd

from RunningScrip.newVariableForPairTrading import createModifiedVariableForPairTrading
from functions.technicalIndicators import *
# Importation des variables transformées
newVariableDataFrame, newVariableToTradeDataFrame = createModifiedVariableForPairTrading(rollingWindow=60, numberOfPairsToTrade=2)

# Création du dataframe pour les indicateurs techniques
indicatorsDataFrame = pd.DataFrame(index=newVariableDataFrame.index)

# Ajout des indicateurs techniques dans le dataframe pour indicateur.
indicatorsDataFrame = indicatorsDataFrame.join(addNewIndicator(aroon, 'aroon', newVariableDataFrame))
indicatorsDataFrame = indicatorsDataFrame.join(addNewIndicator(ADX, 'ADX', newVariableDataFrame))
indicatorsDataFrame = indicatorsDataFrame.join(addNewIndicator(MACD, 'MACD', newVariableDataFrame))
indicatorsDataFrame = indicatorsDataFrame.join(addNewIndicator(RSI, 'RSI', newVariableDataFrame))
indicatorsDataFrame = indicatorsDataFrame.join(addNewIndicator(SMI, 'SMI', newVariableDataFrame))

