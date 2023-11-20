import pandas as pd
import GlobalConfigs
import DataInterpolator

def CleanData(rawData:dict[str, pd.DataFrame]) -> pd.DataFrame:
    print("Beginning the process of cleaning data...")

    # Interpolate
    cfsData = rawData["callsForService"].copy()
    weatherData = DataInterpolator.InterpolateData(rawData["weather"].copy())

    # Merge
    cleanData = __joinDataTables(cfsData, weatherData)

    # Clean
    cleanData = __removeUnnecessaryColumns(cleanData)
    cleanData = __cleanAllText(cleanData)
    __saveCleanData(cleanData)

    print("Completed the process of cleaning data.")

    return cleanData

def __joinDataTables(callsForServiceData:pd.DataFrame, weatherData:pd.DataFrame):
    print("Merging data...")

    # Convert dates in data frames to a consistent format
    callsForServiceData["occ_date"] = pd.to_datetime(callsForServiceData["occ_date"], format="%m/%d/%Y")
    weatherData["DATE"] = pd.to_datetime(weatherData["DATE"], format="%Y-%m-%d")

    combinedData = callsForServiceData.set_index("occ_date").join(weatherData.set_index("DATE"), how="inner")
    combinedData.index.name = "Date"
    return combinedData

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
