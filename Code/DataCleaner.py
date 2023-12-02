import pandas as pd
import GlobalConfigs
import DataInterpolator

def CleanData(rawData:dict[str, pd.DataFrame]) -> pd.DataFrame:
    print("Beginning the process of cleaning data...")

    # Bin
    callsForServiceData = rawData["callsForService"].copy()
    binnedCallsForServiceData = __binData(callsForServiceData)

    # Interpolate
    interpolatedCallsForServiceData = DataInterpolator.InterpolateCallsForServiceData(binnedCallsForServiceData)
    interpolatedWeatherData = DataInterpolator.InterpolateWeatherData(rawData["weather"].copy())

    # Merge
    cleanData = __joinDataTables(interpolatedCallsForServiceData, interpolatedWeatherData)

    # Clean
    cleanData = __removeUnnecessaryColumns(cleanData)
    cleanData = __cleanAllText(cleanData)
    __saveCleanData(cleanData)

    print("Completed the process of cleaning data.")

    return cleanData

def __binData(data:pd.DataFrame) -> pd.DataFrame:
    print("Binning the data...")

    # Bin by day, and then by case decription
    retData = __cleanAllText(data)
    retData = retData.groupby(['occ_date', 'CASE DESC']).size().reset_index(name='Case Count')
    retData.set_index('occ_date')
    
    return retData

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
        "STATION", "NAME",              # Categorical attributes that are the same since we only use one weather station source
        "WDF2", "WDF5", "WSF2", "WSF5", # Numerical attributes that were measured, but we don't care about since we have the average already
        "TMAX", "TMIN",                 # Since we've interpolated the temp averages, we'll remove the min/max temps
        "PSUN", "TSUN", "PGTM"          # Numerical attributes not measured at the weather station
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
