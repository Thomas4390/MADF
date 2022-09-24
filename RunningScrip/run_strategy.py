import numpy as np
import pandas as pd

from Class.RollingWindow import MyRollingWindow
from functions.importationTitres import get_sp_data, importDataFromYahoo
from functions.dataTransformation import transformPricesToYield, find_n_max_pairs, create_variable_to_trade

# Hyperparametres

ROLLING_WINDOW = 60

# Étape 1 : Importer les prix des titres à analyser
# prixTitresSP = get_sp_data()
prixTitres = importDataFromYahoo(['AAPL', 'MSFT', 'META']).dropna(how='any')
# prixTitres = pd.read_hdf('../data/sp_500_data.hdf')

# Étape 2 : Transformation des prix en rendement
yieldTitresSP = transformPricesToYield(prixTitres)

# Étape 3 : Pour que le modèle soit dynamique dans le temps (pas toujours les mêmes paires de titre que l'on transige),
# il faut une rolling window pour l'étape 4 à 8.

rollingWindowData = MyRollingWindow(yieldTitresSP, window=ROLLING_WINDOW)
newVariableDataFrame = pd.DataFrame(index=prixTitres.index)
newVariableToTradeDataFrame = pd.DataFrame(index=prixTitres.index)
for windowData in rollingWindowData:
    # Étape 4 : Analyse de la dépendance (covariance) à chaque période.
    covMat = windowData.corr()

    # Étape 5 : Choisir les "n" paires de titres dépendants pour faire le pair trading.
    # On choisit soit les 'n' plus grandes corrélations ou toutes les paires dont la corrélation est supérieure à un threshold "alpha".
    nPairs = find_n_max_pairs(covMat, n_max=2)

    # Étape 6 : Créer les nouvelles variables "X" à trader / analyser (différence ou ratio entre les paires des PRIX de titres sélectionnées)
    # (A - B) ou (A / B)
    pricesAfterRollingWindow = prixTitres.loc[prixTitres.index > windowData.index[-1], :]
    newVar = create_variable_to_trade(pricesAfterRollingWindow, nPairs)

    #### METTRE DANS UNE NOUVELLE FONCTION POUR QUE "run_strategy.py" SOIT LISIBLE, SINON C'EST LAID À CHIER À TERRE
    columnsToKeep = [True] * newVar.shape[1]
    newColumns = newVar.columns
    if not newVariableDataFrame.empty:
        columnsToKeep = list(map(lambda x: x not in newVariableDataFrame.columns, newColumns))

    for newcol in newColumns[columnsToKeep]:
        newVariableToTradeDataFrame[newcol] = np.nan

    newVariableDataFrame = newVariableDataFrame.join(newVar.loc[:, columnsToKeep])

    newVarNextWindow = newVar.iloc[:ROLLING_WINDOW, :]
    newVariableToTradeDataFrame.loc[newVarNextWindow.index, newColumns] = 1
    ######## FIN DE NOUVELLE FONCTION

    # Étape 7 : Pour chacune des variables "X", on doit trouver des variables explicatives pour prédire le rendement futur.
    # Soit, les lags des rendements, indicateurs techniques, métriques macroéconomiques...

    # Étape 8 : Ajouter les variables explicatives à un dataframe. Append au dataframe pour chaque nouvelle observation / window

    pass

# Étape 9 : Création d'un modèle prédictif.
