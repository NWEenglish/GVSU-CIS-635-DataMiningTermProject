import DataVisualizer
import GlobalConfigs
import numpy as np
import pandas as pd
from sklearn import neighbors, tree
from sklearn.model_selection import StratifiedKFold, cross_val_score
from scipy.stats import chi2_contingency, pearsonr

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
    print("Beginning the process of finding correlations in the data...")

    caseTypes = data['CASE DESC'].unique()
    caseTypes.sort()

    correlationTable = pd.DataFrame(columns=data.columns)
    correlationTable['CASE DESC'] = caseTypes
    correlationTable.set_index('CASE DESC', inplace=True)
    correlationTable.drop(columns=['Count Category'], inplace=True)

    for caseType in caseTypes:
        __correlationAnalysis(data, caseType, correlationTable)

    correlationTable.to_csv(GlobalConfigs.CORRELATION_ANALYSIS_FILEPATH)

    print("Completed the process of finding correlations in the data.")

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

def __correlationAnalysis(data:pd.DataFrame, caseType:str, correlationTable:pd.DataFrame) -> None:
    print(f"Performing correlation analysis for {caseType}...")
    
    thisData = data.copy()
    thisData = thisData.loc[data['CASE DESC'] == caseType].reset_index(drop=True)

    __continuousWeatherCorrelationAnalysis(thisData, caseType, correlationTable)
    __weatherTypeCorrelationAnalysis(thisData, caseType, correlationTable)
    
def __continuousWeatherCorrelationAnalysis(data:pd.DataFrame, caseType:str, correlationTable:pd.DataFrame):
    thisData = data.copy()
    thisData['Count Category'] = thisData['Count Category'].astype('category').cat.codes
    significanceThreshold = 0.05

    # Continuous values will use Pearson for correlation analysis
    for weatherColumn in ['AWND', 'PRCP','SNOW','SNWD', 'TAVG']:
        correlation, pValue = pearsonr(thisData[weatherColumn], thisData['Count Category'])

        if (pValue <= significanceThreshold):
            correlationTable.at[caseType, weatherColumn] = 'X'
            print(f'Results suggest a significant relationship between {caseType} and {weatherColumn}. | {pValue} <= {significanceThreshold}')

def __weatherTypeCorrelationAnalysis(data:pd.DataFrame, caseType:str, correlationTable:pd.DataFrame):
    significanceThreshold = 0.05

    # Weather Type columns will use chi2 test for correlation analysis since they have binary outputs
    for weatherType in ['WT01', 'WT02', 'WT03', 'WT04', 'WT05', 'WT06', 'WT08', 'WT09', 'WT10', 'WT13', 'WT14', 'WT16', 'WT18', 'WT21', 'WT22']:
        contingencyTable = pd.crosstab(data['Count Category'], data[weatherType])
        chi2Result = chi2_contingency(observed=contingencyTable)

        if (chi2Result.pvalue <= significanceThreshold):
            correlationTable.at[caseType, weatherType] = 'X'
            print(f'Results suggest a significant relationship between {caseType} and {weatherType}. | {chi2Result.pvalue} <= {significanceThreshold}')
