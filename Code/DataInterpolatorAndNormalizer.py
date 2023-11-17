import pandas as pd
import GlobalConfigs

def InterpolateAndNormalizeData(cleanData:pd.DataFrame) -> pd.DataFrame:
    print("Beginning the process of interpolating and normalizing the data...")

    normalizedData = __interpolateData(cleanData)
    normalizedData = __normalizeData(normalizedData)
    __saveNormalizedData(normalizedData)

    print("Completed the process of interpolating and normalizing the data.")

    return normalizedData

def __interpolateData(data:pd.DataFrame) -> pd.DataFrame:
    print("Interpolating the data...")
    retData = data.copy() # TODO: Add logic
    return retData

def __normalizeData(data:pd.DataFrame) -> pd.DataFrame:
    print("Normalizing the data...")
    retData = data.copy() # TODO: Add logic
    return retData

def __saveNormalizedData(data:pd.DataFrame):
    print("Saving normalized data...")
    data.to_csv(GlobalConfigs.NORMALIZED_DATA_FILEPATH)
