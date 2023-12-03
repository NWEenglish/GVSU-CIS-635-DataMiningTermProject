import numpy as np
import pandas as pd

def BinCallsForServiceByCaseData(data:pd.DataFrame) -> pd.DataFrame:
    print("Binning Calls-for-Service by dates and case types data...")
    retData = data.copy()

    # Bin by day, and then by case decription
    retData = retData.groupby(['occ_date', 'CASE DESC']).size().reset_index(name='Case Count')
    retData.set_index('occ_date')

    return retData

def BinCallsForServiceByClassifyingData(data:pd.DataFrame) -> pd.DataFrame:
    print("Binning Calls-for-Service by classifying above/about/below normal...")
    retData = data.copy()
    
    # Bin by case type with if above, below, or within the average.
    for caseType in retData['CASE DESC'].unique():
        retData = __classifyCaseCount(retData, caseType)

    return retData

def __classifyCaseCount(data:pd.DataFrame, caseType:str) -> pd.DataFrame:
    retData = data.copy()

    columnData = data[data['CASE DESC'] == caseType]['Case Count']

    max = columnData.max()
    min = 0
    median = columnData.median()

    aboveNormal = ((max - median) / 2) + median
    belowNormal = ((median - min) / 2) + min

    retData.loc[(retData['CASE DESC'] == caseType) & (retData['Case Count'] > aboveNormal), 'Count Category'] = 1 # Above Normal
    retData.loc[(retData['CASE DESC'] == caseType) & (retData['Case Count'] < belowNormal), 'Count Category'] = 0 # Below Normal
    retData.loc[(retData['CASE DESC'] == caseType) & (retData['Case Count'] >= belowNormal) & (retData['Case Count'] <= aboveNormal), 'Count Category'] = .5 # About Normal

    return retData
