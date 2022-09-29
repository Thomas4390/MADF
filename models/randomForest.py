import numpy as np
from sklearn.model_selection import TimeSeriesSplit
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics

from RunningScrip.technicalIndicators import getData

# On fait de la classification avec random forest.
# La variable réponse est 1 si la valeur réponse est supérieur à zéro et est zéro autrement.

newVariableDataFrame, newVariableToTradeDataFrame, indicatorsDataFrame = getData(
    rollingWindow=60, numberOfPairsToTrade=2, method="alphaFactor"
)

y = (newVariableDataFrame > newVariableDataFrame.shift(1)).shift(
    -1
)  # on veut prédire le lendemain
y = newVariableToTradeDataFrame * y
indicatorsDataFrame.iloc[-1, :] = np.nan
x = indicatorsDataFrame * newVariableToTradeDataFrame.to_numpy()

tscv = TimeSeriesSplit()
for train_index, test_index in tscv.split(x):
    X_train, X_test = x.iloc[train_index, :], x.iloc[test_index, :]
    y_train, y_test = y.iloc[train_index, :], y.iloc[test_index, :]


y_train = y_train.melt()["value"].dropna(how="any").apply(lambda x: int(x))
y_test = y_test.melt()["value"].dropna(how="any").apply(lambda x: int(x))

X_train = X_train.melt()["value"].dropna(how="any")
X_test = X_test.melt()["value"].dropna(how="any")

modForestClass = RandomForestClassifier(n_estimators=300, random_state=0)
modForestClass.fit(X_train.to_numpy().reshape(-1, 1), y_train.to_numpy())


fpr, tpr, thresholds = metrics.roc_curve(
    y_test.to_numpy(),
    modForestClass.predict(X_test.to_numpy().reshape(-1, 1)),
    pos_label=1,
)
print(metrics.auc(fpr, tpr))
