from typing import Tuple

import numpy as np
import pandas as pd

from Class.RollingWindow import MyRollingWindow
from functions.importationTitres import get_sp_data, importDataFromYahoo
from functions.dataTransformation import transformPricesToYield, find_n_max_pairs, create_variable_to_trade


# Hyperparametres


def createModifiedVariableForPairTrading(
    rollingWindow: int = 60, numberOfPairsToTrade: int = 2, method="diff"
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    # Étape 1 : Importer les prix des titres à analyser
    # prixTitresSP = get_sp_data()
    prixTitres = importDataFromYahoo(['AAPL', 'MSFT', 'META']).dropna(how='any')
    # prixTitres = pd.read_hdf('../data/sp_500_data.hdf')

    # Étape 2 : Transformation des prix en rendement
    yieldTitresSP = transformPricesToYield(prixTitres)

    # Étape 3 : Pour que le modèle soit dynamique dans le temps (pas toujours les mêmes paires de titre que l'on transige),
    # il faut une rolling window pour l'étape 4 à 8.

    rollingWindowData = MyRollingWindow(yieldTitresSP, window=rollingWindow)
    newVariableDataFrame = pd.DataFrame(index=prixTitres.index)
    newVariableToTradeDataFrame = pd.DataFrame(index=prixTitres.index)
    variableAlreadyCalculated = []
    for windowData in rollingWindowData:
        # Étape 4 : Analyse de la dépendance (covariance) à chaque période.
        covMat = windowData.corr()

        # Étape 5 : Choisir les "n" paires de titres dépendants pour faire le pair trading.
        # On choisit soit les 'n' plus grandes corrélations ou toutes les paires dont la corrélation est supérieure à un threshold "alpha".
        nPairs = find_n_max_pairs(covMat, n_max=numberOfPairsToTrade)

        # Étape 6 : Créer les nouvelles variables "X" à trader / analyser (différence ou ratio entre les paires des PRIX de titres sélectionnées)
        # (A - B) ou (A / B)
        pricesAfterRollingWindow = prixTitres.loc[
                                   prixTitres.index > windowData.index[-1], :
                                   ]
        windowToTrade = pricesAfterRollingWindow.index[:rollingWindow]
        if not newVariableDataFrame.empty:
            columnsToKeep = list(
                map(lambda x: x not in variableAlreadyCalculated, nPairs)
            )
        else:
            columnsToKeep = [True] * len(nPairs)
        variableToKeep = [nPairs[i] for i, x in enumerate(columnsToKeep) if x]
        variableAlreadyCalculated += variableToKeep
        newVar = create_variable_to_trade(prixTitres, variableToKeep, method=method)

        # TODO: METTRE DANS UNE NOUVELLE FONCTION POUR QUE "run_strategy.py" SOIT LISIBLE, SINON C'EST LAID À CHIER À TERRE
        columnsToKeep = [True] * newVar.shape[1]
        newColumns = newVar.columns
        # if not newVariableDataFrame.empty:
        #     columnsToKeep = list(
        #         map(lambda x: x not in newVariableDataFrame.columns, newColumns)
        #     )

        for newcol in newColumns[columnsToKeep]:
            newVariableToTradeDataFrame[newcol] = np.nan

        # newVariableDataFrame = newVariableDataFrame.join(newVar.loc[:, columnsToKeep])
        newVariableDataFrame = newVariableDataFrame.join(
            newVar)

        # newVarNextWindow = newVar.iloc[:rollingWindow, :]
        # newVariableToTradeDataFrame.loc[newVarNextWindow.index, newColumns] = 1
        newVariableToTradeDataFrame.loc[windowToTrade, newColumns] = 1

        ######## FIN DE NOUVELLE FONCTION
    return newVariableDataFrame, newVariableToTradeDataFrame

    # Étape 7 : Pour chacune des variables "X", on doit trouver des variables explicatives pour prédire le rendement futur.
    # Soit, les lags des rendements, indicateurs techniques, métriques macroéconomiques...

    # Étape 8 : Ajouter les variables explicatives à un dataframe. Append au dataframe pour chaque nouvelle observation / window

    # Étape 9 : Création d'un modèle prédictif.
