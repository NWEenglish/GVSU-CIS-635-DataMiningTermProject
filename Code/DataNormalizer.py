import pandas as pd
import GlobalConfigs
from sklearn.preprocessing import MinMaxScaler

def NormalizeData(cleanData:pd.DataFrame) -> pd.DataFrame:
    print("Beginning the process of normalizing the data...")

    normalizedData = __normalizeData(cleanData)
    __saveNormalizedData(normalizedData)

    print("Completed the process of normalizing the data.")

    return normalizedData

def __normalizeData(data:pd.DataFrame) -> pd.DataFrame:
    print("Normalizing the data...")
    retData = data.copy()

    # Change CASE DESC from categorical to numerical code
    retData['Case Desc Code'] = retData['CASE DESC'].cat.codes

    # Using min-max for numerical attributes known to not be on the same scale
    minMaxScale = 1
    for column in ['Case Desc Code', 'AWND', 'PRCP', 'SNOW', 'SNWD', 'TAVG']:
        retData = __minMaxNormalizer(retData, column, minMaxScale)

    return retData

def __minMaxNormalizer(data:pd.DataFrame, column:str, scale:int) -> pd.DataFrame:
    retData = data.copy()
    
    # If the range does not show we're in scale, then perform min-max
    range = retData[column].max() - retData[column].min()
    if range > scale:
        minMaxScaler = MinMaxScaler()
        retData[column] = minMaxScaler.fit_transform(retData[[column]])

    return retData

def __saveNormalizedData(data:pd.DataFrame):
    print("Saving normalized data...")
    data.to_csv(GlobalConfigs.NORMALIZED_DATA_FILEPATH)
