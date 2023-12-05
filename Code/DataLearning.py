import DataVisualizer
import numpy as np
import pandas as pd
from sklearn import neighbors, tree
from sklearn.model_selection import StratifiedKFold, cross_val_score

class LearnedModels():
    stateValue:int = 616
    KnnModel = None
    KnnModelScore = 0
    DecisionTree = None
    DecisionTreeScore = 0
    Columns = [str]

    def __init__(self):
        self.KnnModel = neighbors.KNeighborsClassifier()
        self.DecisionTree = tree.DecisionTreeClassifier(max_depth=5)


def LearnAndTest(data:pd.DataFrame) -> dict[str, LearnedModels]:
    print("Beginning the process of learning and testing the data...")

    retLearnedModels = {}
    caseTypes = data['CASE DESC'].unique()
    caseTypes.sort()

    for caseType in caseTypes:
        retLearnedModels[caseType] = __learningAndTesting(data, caseType)

    print("Completed the process of learning and testing the data.")
    return retLearnedModels

def Graph(models:dict[str, LearnedModels]) -> None:
    print("Beginning the process of graphing the models...")

    caseTypes = models.keys()
    for caseType in caseTypes:
        DataVisualizer.DecisionTree(models[caseType].Columns, models[caseType].DecisionTree, caseType)

    print("Completed the process of graphing the models.")

def CorrelationAnalysis(data:pd.DataFrame) -> None:
    print("TODO x^2")

# Previously planned on using info gain, but realize since I want the tree anyways then using the decision tree model makes more sense.
def __learningAndTesting(dataToLearn:pd.DataFrame, caseType:str) -> LearnedModels:
    print(f"Performing KNN and Decision Tree learning for '{caseType}'...")
    data = dataToLearn.copy()
    data = data.loc[data['CASE DESC'] == caseType].reset_index(drop=True)
    retModels = LearnedModels()

    # Setup K-folds
    skf = StratifiedKFold(n_splits=4, shuffle=True, random_state=retModels.stateValue)
    y = data['Count Category']
    X = data.drop(columns=['Count Category', 'CASE DESC']) # Includes more cleaning that had to come later
    retModels.Columns = X.columns

    # Begin training models    
    for train_index, test_index in skf.split(X, y):
        X_train = X.loc[train_index]
        y_train = y.loc[train_index]

        retModels.KnnModel.fit(X_train, y_train)
        retModels.DecisionTree.fit(X_train, y_train)

    # Test the trained models
    print(f"Performing KNN and Decision Tree testing for '{caseType}'...")

    # Change scoring since classes will be in-balanced
    retModels.KnnModelScore = np.mean(cross_val_score(retModels.KnnModel, X, y, cv=skf.get_n_splits(), scoring='f1_micro'))
    retModels.DecisionTreeScore = np.mean(cross_val_score(retModels.DecisionTree, X, y, cv=skf.get_n_splits(), scoring='f1_micro'))

    print(f"Scores for {caseType} -> KNN = {retModels.KnnModelScore}; Decision Tree = {retModels.DecisionTreeScore}")

    return retModels

# Look at HW #2
def __correlationAnalysis(data:pd.DataFrame) -> None:
    print("Performing correlation analysis with x^2...")