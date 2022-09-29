from typing import Optional, Tuple, Iterator, Dict

import pandas as pd


class MyRollingWindow(Iterator):
    def __init__(self, df: pd.DataFrame, window: int, i: int = 0):
        self.df = df
        self.window = window
        self.i = i
        self.numberObs = df.shape[0]

    def __next__(self) -> pd.DataFrame:
        fromIdx = self.i * self.window
        toIdx = (self.i + 1) * self.window
        if fromIdx > self.numberObs:
            self.i = 0
            raise StopIteration

        elif toIdx > self.numberObs:
            toIdx = self.numberObs

        self.i += 1

        return self.df.iloc[fromIdx:toIdx, :]


class RollingDataSet:
    # def __init__(
    #     self,
    #     trainData: Dict[int, pd.DataFrame],
    #     testData: Dict[int, Dict[Literal[0, 1], Optional[pd.DataFrame]]],
    #     numberFolds: int,
    # ):
    #     """
    #     :param trainData : Un dictionnaire dont la clé est le fold number et item est le train dataframe
    #     :param testData : Un dictionnaire dont la clé est le fold number et item un autre dictionnaire.
    #     Si la clé du deuxième dictionnaire est 0, alors son item est le test set qui était temporellement avant le train set.
    #     Si la clé du deuxième dictionnaire est 1, alors son item est le test set qui était temporellement après le train set.
    #     :param numberFolds : nombre de folds
    #     """
    #     self.trainData = trainData
    #     self.testData = testData
    #     self.numberFolds = numberFolds
    #     self.foldsRemaining = numberFolds
    #     self.nextFold = 0
    #
    # def __iter__(self):
    #     return self
    #
    # def __next__(
    #     self,
    # ) -> Tuple[pd.DataFrame, Dict[Literal[0, 1], Optional[pd.DataFrame]]]:
    #     """
    #     Permet d'obtenir le train et test set d'un fold à chaque itération.
    #     :return : trainSet, testSet
    #     """
    #     if self.foldsRemaining == 0:
    #         # Permet de pouvoir re-call une iteration sur la classe
    #         self.foldsRemaining = self.numberFolds
    #         self.nextFold = 0
    #         raise StopIteration
    #
    #     trainDataToReturn = self.trainData[self.nextFold]
    #     testDataToReturn = {
    #         0: self.testData[self.nextFold][0],
    #         1: self.testData[self.nextFold][1],
    #     }
    #
    #     self.foldsRemaining -= 1
    #     self.nextFold += 1
    #
    #     return trainDataToReturn, testDataToReturn
    pass
