from typing import Tuple, Dict, Any, Union, Literal, Optional

import numpy as np
import pandas as pd


class CrossValidationData:
    def __init__(
        self,
        trainData: Dict[int, pd.DataFrame],
        testData: Dict[int, Dict[Literal[0, 1], Optional[pd.DataFrame]]],
        numberFolds: int,
    ):
        """
        :param trainData : Un dictionnaire dont la clé est le fold number et item est le train dataframe
        :param testData : Un dictionnaire dont la clé est le fold number et item un autre dictionnaire.
        Si la clé du deuxième dictionnaire est 0, alors son item est le test set qui était temporellement avant le train set.
        Si la clé du deuxième dictionnaire est 1, alors son item est le test set qui était temporellement après le train set.
        :param numberFolds : nombre de folds
        """
        self.trainData = trainData
        self.testData = testData
        self.numberFolds = numberFolds
        self.foldsRemaining = numberFolds
        self.nextFold = 0

    def __iter__(self):
        return self

    def __next__(
        self,
    ) -> Tuple[pd.DataFrame, Dict[Literal[0, 1], Optional[pd.DataFrame]]]:
        """
        Permet d'obtenir le train et test set d'un fold à chaque itération.
        :return : trainSet, testSet
        """
        if self.foldsRemaining == 0:
            # Permet de pouvoir re-call une iteration sur la classe
            self.foldsRemaining = self.numberFolds
            self.nextFold = 0
            raise StopIteration

        trainDataToReturn = self.trainData[self.nextFold]
        testDataToReturn = {
            0: self.testData[self.nextFold][0],
            1: self.testData[self.nextFold][1],
        }

        self.foldsRemaining -= 1
        self.nextFold += 1

        return trainDataToReturn, testDataToReturn


def crossValidationSplitForTimeSeries(
    data: pd.DataFrame, numberFolds: int = 5, cushion: int = 0
) -> CrossValidationData:
    """
    Permet de créer split la base de donnée en "n" folds pour ensuite faire la cross validation. Le jeu empiète sur le test set
    :param cushion : Nombre d'observations à ne pas considérer entre le train et test set
    :param data : Base de données à split
    :param numberFolds : Le nombre de fois qu'on veut séparer les données
    :return : CrossValidationData pour faire la cross validation
    """

    if not isinstance(data, pd.DataFrame):
        raise Exception("data is not pd.DataFrame")

    if not isinstance(data.index, pd.DatetimeIndex):
        raise Exception("Index should be pd.Datetime")

    trainData: Dict[int, Any] = {}
    testData = {}
    trainLength = int(np.ceil(data.shape[0] / numberFolds))

    if trainLength <= cushion:
        raise Exception(
            "cushion is too big for the number of folds. Choose a smaller cushion or smaller numberFolds"
        )

    for fold in range(numberFolds):
        testData[fold] = {}
        trainData[fold] = data.iloc[
            (fold * trainLength) : ((fold + 1) * trainLength), :
        ]

        # Si premier pli, il n'y a pas de test data avant le train
        if fold == 0:
            testData[fold][0] = None
        else:
            testData[fold][0] = data.iloc[: (fold * trainLength - cushion), :]

        # Si dernier pli, il n'y a pas de test data après le train.
        if fold == numberFolds - 1:
            testData[fold][1] = None
        else:
            testData[fold][1] = data.iloc[((fold + 1) * trainLength + cushion) :, :]

    return CrossValidationData(trainData, testData, numberFolds)
