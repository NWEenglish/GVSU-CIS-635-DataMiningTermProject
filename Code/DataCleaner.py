import pandas as pd
import GlobalConfigs

def CleanData(rawData:pd.DataFrame) -> pd.DataFrame:
    print("Beginning the process of cleaning data...")

    cleanData = __removeUnnecessaryColumns(rawData)
    cleanData = __cleanAllText(cleanData)
    __saveCleanData(cleanData)

    print("Completed the process of cleaning data.")

    return cleanData

def __removeUnnecessaryColumns(data:pd.DataFrame) -> pd.DataFrame:
    print("Removing unnecessary columns...")

    retData = data.copy()
    retData = retData.drop(columns=[
        "x_coordinate", "y_coordinate", "census_tract", "STATION", "NAME",      # Values we don't care about
        "PSUN", "TSUN", "PGTM"                                                  # Values not measured at the weather station
    ])

    return retData

def __cleanAllText(data:pd.DataFrame) -> pd.DataFrame:
    print("Cleaning text values...")
    
    # Removes leading/trailing whitespace and unnecessary text
    retData = data.copy().applymap(lambda x: x.strip().replace(" - COLD", '') if isinstance(x, str) else x)
    return retData

def __saveCleanData(data:pd.DataFrame):
    print("Saving cleaned data...")
    data.to_csv(GlobalConfigs.CLEANED_DATA_FILEPATH)
