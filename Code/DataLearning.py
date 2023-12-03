import DataVisualizer
import pandas as pd
from sklearn import neighbors, tree
from sklearn.model_selection import StratifiedKFold

class LearnedModels():
    stateValue:int = 616
    KnnModel = neighbors.KNeighborsClassifier()
    DecisionTree = tree.DecisionTreeClassifier()
    Columns = [str]

def LearnAndTest(data:pd.DataFrame) -> None:
    print("Beginning the process of learning the data...")

    # Learn models
    retModels = __learning(data)

    # Output graphs
    DataVisualizer.DecisionTree(retModels.Columns, retModels.DecisionTree)

    # Test models

    print("Completed the process of learning the data.")

# Look at HW #3
# Previously planned on using info gain, but realize since I want the tree anyways then using the decision tree model makes more sense.
def __learning(dataToLearn:pd.DataFrame) -> LearnedModels:
    print("Performing KNN and Decision Tree learning...")
    data = dataToLearn.copy()
    retModels = LearnedModels

    # Setup K-folds
    skf = StratifiedKFold(n_splits=4, shuffle=True, random_state=retModels.stateValue)
    y = data['Count Category'].reset_index(drop=True)
    X = data.drop(columns=['Count Category', 'Date', 'CASE DESC']).reset_index(drop=True) # Includes more cleaning that had to come later
    retModels.Columns = X.columns

    # Begin training models    
    for train_index, test_index in skf.split(X, y):
        X_train = X.loc[train_index]
        y_train = y.loc[train_index]

        retModels.KnnModel.fit(X_train, y_train)
        retModels.DecisionTree.fit(X_train, y_train)

    return retModels

# Look at HW #3
def __testModels(data:pd.DataFrame) -> None:
    print("Beginning the process of testing the learned models...")

# Look at HW #2
def __correlationAnalysis(data:pd.DataFrame) -> None:
    print("Performing correlation analysis with x^2...")