import pandas as pd
import GlobalConfigs

def NormalizeData(cleanData:pd.DataFrame) -> pd.DataFrame:
    print("Beginning the process of normalizing the data...")

    normalizedData = __normalizeData(cleanData)
    __saveNormalizedData(normalizedData)

    print("Completed the process of normalizing the data.")

    return normalizedData

def __normalizeData(data:pd.DataFrame) -> pd.DataFrame:
    print("Normalizing the data...")
    retData = data.copy() # TODO: Add logic
    return retData

def __saveNormalizedData(data:pd.DataFrame):
    print("Saving normalized data...")
    data.to_csv(GlobalConfigs.NORMALIZED_DATA_FILEPATH)
