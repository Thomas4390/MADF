import pandas as pd

from RunningScrip.newVariableForPairTrading import createModifiedVariableForPairTrading
from functions.functionsTechnicalIndicators import *

newVariableDataFrame, newVariableToTradeDataFrame = createModifiedVariableForPairTrading(rollingWindow=60, numberOfPairsToTrade=2)
indicatorsDataFrame = pd.DataFrame(index=newVariableDataFrame.index)

indicatorsDataFrame = indicatorsDataFrame.join(addNewIndicator(AROON, 'AROON', newVariableDataFrame, period=25))
# indicatorsDataFrame = indicatorsDataFrame.join(addNewIndicator(ADX, 'ADX', newVariableDataFrame))
# indicatorsDataFrame = indicatorsDataFrame.join(addNewIndicator(MACD, 'MACD', newVariableDataFrame))
# indicatorsDataFrame = indicatorsDataFrame.join(addNewIndicator(RSI, 'RSI', newVariableDataFrame))
# indicatorsDataFrame = indicatorsDataFrame.join(addNewIndicator(SMI, 'SMI', newVariableDataFrame))

print(indicatorsDataFrame)

