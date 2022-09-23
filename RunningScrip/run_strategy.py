from functions.importationTitres import get_sp_data
from functions.dataTransformation import transformPricesToYield, createRollingData

# Étape 1 : Importer les prix des titres à analyser
prixTitresSP = get_sp_data(pass)

# Étape 2 : Transformation des prix en rendement
yieldTitresSP = transformPricesToYield(pass)

# Étape 3 : Pour que le modèle soit dynamique dans le temps (pas toujours les mêmes paires de titre que l'on transige),
# il faut une rolling window pour l'étape 4 à 8.

rollingWindowData = createRollingData()


for windowData in rollingWindowData:
    # Étape 4 : Analyse de la dépendance (covariance) à chaque période.

    covMat = windowData.cov()

    # Étape 5 : Choisir les "n" paires de titres dépendants pour faire le pair trading.
    # On choisit soit les 'n' plus grandes corrélations ou toutes les paires dont la corrélation est supérieure à un threshold "alpha".



    # Étape 6 : Créer les nouvelles variables "X" à trader / analyser (différence ou ratio entre les paires des PRIX de titres sélectionnées)
    # (A - B) ou (A / B)



    # Étape 7 : Pour chacune des variables "X", on doit trouver des variables explicatives pour prédire le rendement futur.
    # Soit, les lags des rendements, indicateurs techniques, métriques macroéconomiques...

    # Étape 8 : Ajouter les variables explicatives à un dataframe. Append au dataframe pour chaque nouvelle observation / window

    pass

# Étape 9 : Création d'un modèle prédictif.
