from typing import Tuple
import numpy as np
import pandas as pd

from Class.RollingWindow import MyRollingWindow
from functions.importationTitres import read_sp_data, importDataFromYahoo
from functions.dataTransformation import (
    transformPricesToYield,
    find_n_max_pairs,
    create_variable_to_trade,
)


# Hyperparametres


def createModifiedVariableForPairTrading(
    rollingWindow: int = 60, numberOfPairsToTrade: int = 2, method="norm"
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    # Étape 1 : Importer les prix des titres à analyser
    # prixTitres = importDataFromYahoo(["AAPL", "MSFT", "META"]).dropna(how="any")
    prixTitres = read_sp_data()

    # Étape 2 : Transformation des prix en rendement pour calculer la matrice de corrélation
    yieldTitresSP = transformPricesToYield(prixTitres)

    # Étape 3 : Pour que le modèle soit dynamique dans le temps (pas toujours les mêmes paires de titre que l'on transige),
    # il faut une rolling window pour l'étape 4 à 8.

    rollingWindowData = MyRollingWindow(yieldTitresSP, window=rollingWindow)
    newVariableDataFrame = pd.DataFrame(index=prixTitres.index)
    newVariableToTradeDataFrame = pd.DataFrame(index=prixTitres.index)
    variableAlreadyCalculated = []
    for windowData in rollingWindowData:

        # Étape 4 : Analyse de la dépendance (covariance) à chaque période.
        covMat = windowData.corr().fillna(0)

        # Étape 5 : Choisir les "n" paires de titres dépendants pour faire le pair trading.
        # On choisit soit les 'n' plus grandes corrélations ou toutes les paires dont la corrélation est supérieure à un threshold "alpha".

        nPairs = find_n_max_pairs(covMat, n_max=numberOfPairsToTrade)

        # Étape 6 : Créer les nouvelles variables "X" à trader / analyser (différence ou ratio entre les paires des PRIX de titres sélectionnées)
        # (A - B) ou (A / B)

        # On prend les prix uniquement après la la rollingWindow (sur laquelle a été calculé la matrice de corrélation)
        # pour pouvoir garder en mémoire à quel moment on trade quel titre.
        pricesAfterRollingWindow = prixTitres.loc[
            prixTitres.index > windowData.index[-1], :
        ]

        # La window sur laquelle on trade nos titres (n jours après la fin de la dernière rollingWindow)
        windowToTrade = pricesAfterRollingWindow.index[:rollingWindow]

        # Pour ne pas calculer les nouvelles variables avec toutes les combinaisons (paires) de titres, on calcul la nouvelle variable
        # uniquement avec les paires qui ont la plus grande corrélation. Si on calcul une paire, on la calculera pout toute la timeseries
        # et non pas juste pour la window puisqu'il va falloir calculer des indicateurs techniques sur des données avant le début de la rolling Window.

        if not newVariableDataFrame.empty: # si ce n'est pas la première nouvelle variable (paire) que l'on crée.
            columnsToKeep = list( # columns to keep représente les colonnes (paires) que l'on a pas déja calculé avec un bool ex: [True, False, ...]
                map(lambda x: x not in variableAlreadyCalculated, nPairs)
            )
        else: # Si c'est la première variable (paire), on garde toute les paires qui on une corrélation maximale.
            columnsToKeep = [True] * len(nPairs)

        variableToKeep = [nPairs[i] for i, x in enumerate(columnsToKeep) if x] # Permet d'avoir une liste des paires déja calculé
        variableAlreadyCalculated += variableToKeep
        newVar = create_variable_to_trade(prixTitres, variableToKeep, method=method) # Création des nouvelles paires/variables


        #TODO: METTRE DANS UNE NOUVELLE FONCTION POUR QUE "run_strategy.py" SOIT LISIBLE, SINON C'EST LAID À CHIER À TERRE

        newColumns = newVar.columns # nouvelle paires de variables

        # columnsToKeep = [True] * newVar.shape[1]
        # if not newVariableDataFrame.empty:
        #     columnsToKeep = list(
        #         map(lambda x: x not in newVariableDataFrame.columns, newColumns)
        #     )

        # TODO: Vérifier si ça fonctionne: newColumns[columnsToKeep]

        for newcol in list(newColumns): # pour les nouvelles paires, on ajoute une colonne de cette paire qui
        # est NAN partout et on mettre des 1 où on trade cette paire.
            newVariableToTradeDataFrame[newcol] = np.nan

        # newVariableDataFrame = newVariableDataFrame.join(newVar.loc[:, columnsToKeep])
        newVariableDataFrame = newVariableDataFrame.join(
            newVar)

        # newVarNextWindow = newVar.iloc[:rollingWindow, :]
        # newVariableToTradeDataFrame.loc[newVarNextWindow.index, newColumns] = 1
        for pair in nPairs:
            newVariableToTradeDataFrame.loc[windowToTrade, f"{pair[0]}-{pair[1]}"] = 1 # Ajoute un 1 quand on trade la paire

        ######## FIN DE NOUVELLE FONCTION
    return newVariableDataFrame, newVariableToTradeDataFrame

    # Étape 7 : Pour chacune des variables "X", on doit trouver des variables explicatives pour prédire le rendement futur.
    # Soit, les lags des rendements, indicateurs techniques, métriques macroéconomiques...

    # Étape 8 : Ajouter les variables explicatives à un dataframe. Append au dataframe pour chaque nouvelle observation / window

    # Étape 9 : Création d'un modèle prédictif.
