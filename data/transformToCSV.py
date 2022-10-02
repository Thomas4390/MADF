import pandas as pd

indicators = pd.read_pickle('../data/indicatorsDataFrame_60_2.pkl')
variablePairs = pd.read_pickle('../data/newVariableDataFrame_60_2.pkl')
variableToTrade = pd.read_pickle('../data/newVariableToTradeDataFrame_60_2.pkl')

indicators.to_csv('../data/indicatorsDataFrame_60_2.csv')
variablePairs.to_csv('../data/newVariableDataFrame_60_2.csv')
variableToTrade.to_csv('../data/newVariableToTradeDataFrame_60_2.csv')