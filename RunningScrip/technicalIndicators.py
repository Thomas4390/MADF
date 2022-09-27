import matplotlib.pyplot as plt
import pandas as pd

from RunningScrip.newVariableForPairTrading import createModifiedVariableForPairTrading
from functions.technicalIndicators import *
# Importation des variables transformées
newVariableDataFrame, newVariableToTradeDataFrame = createModifiedVariableForPairTrading(rollingWindow=250,
                                                                                         numberOfPairsToTrade=2,
                                                                                         method='alphaFactor')
print(type(newVariableDataFrame[newVariableToTradeDataFrame.columns[0]]))
# Création du dataframe pour les indicateurs techniques
indicatorsDataFrame = pd.DataFrame(index=newVariableDataFrame.index)

# Ajout des indicateurs techniques dans le dataframe pour indicateur.
indicatorsDataFrame = indicatorsDataFrame.join(addNewIndicator(aroon, 'aroon', newVariableDataFrame))
#indicatorsDataFrame = indicatorsDataFrame.join(addNewIndicator(MOM, 'MOM', newVariableDataFrame))
mom = TRIX(newVariableDataFrame[newVariableToTradeDataFrame.columns[0]])
print(mom.tail(20))
# indicatorsDataFrame = indicatorsDataFrame.join(addNewIndicator(ADX, 'ADX', newVariableDataFrame))
# indicatorsDataFrame = indicatorsDataFrame.join(addNewIndicator(MACD, 'MACD', newVariableDataFrame))
# indicatorsDataFrame = indicatorsDataFrame.join(addNewIndicator(RSI, 'RSI', newVariableDataFrame))
# indicatorsDataFrame = indicatorsDataFrame.join(addNewIndicator(SMI, 'SMI', newVariableDataFrame))


for column in newVariableDataFrame.columns:
    plt.plot(np.log(1+newVariableDataFrame[column]), label=column)
plt.legend()

# fig, ax = plt.subplots(2)
# for column in newVariableDataFrame.columns:
#     ax[0].plot(newVariableDataFrame[column], label=column)
# ax[0].legend()

# for column in indicatorsDataFrame.columns:
#     ax[1].plot(indicatorsDataFrame[column], label=column)
# ax[1].plot(indicatorsDataFrame.iloc[:, 1], label=indicatorsDataFrame.columns[1])
# ax[1].legend()

plt.show()
