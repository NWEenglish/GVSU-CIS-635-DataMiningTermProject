import pandas as pd
import os
import GlobalConfigs

def ImportRawData() -> pd.DataFrame:
    print("Beginning the process of importing raw data...")

    cfsData = __processCallsForServiceData()
    wData = __processWeatherData()
    joinedData = __joinDataTables(cfsData, wData)

    print("Completed the process of importing raw data.")

    return joinedData

def ImportCleanData() -> pd.DataFrame:
    print("Beginning the process of importing clean data...")
    cleanData = __processCleanData()
    print("Completed the process of importing clean data.")

    return cleanData

def __processCleanData() -> pd.DataFrame:
    print("Reading in clean data...")
    retData = pd.read_csv(GlobalConfigs.CLEAN_DATA_FILEPATH)
    return retData

def __processCallsForServiceData() -> pd.DataFrame:
    print("Reading in Calls-for-Service data...")

    retData = pd.DataFrame()

    for file in os.listdir(GlobalConfigs.RAW_DATA_FOLDER):
        if file.startswith("NIJ"):
            retData = pd.concat([retData, pd.read_csv(GlobalConfigs.RAW_DATA_FOLDER + file)])

    return retData

def __processWeatherData() -> pd.DataFrame:
    print("Reading in Weather data...")
    retData = pd.read_csv(GlobalConfigs.RAW_DATA_FOLDER + "NOAA_Weather.csv")
    return retData

def __joinDataTables(callsForServiceData:pd.DataFrame, weatherData:pd.DataFrame):
    print("Merging data...")

    # Convert dates in data frames to a consistent format
    callsForServiceData["occ_date"] = pd.to_datetime(callsForServiceData["occ_date"], format="%m/%d/%Y")
    weatherData["DATE"] = pd.to_datetime(weatherData["DATE"], format="%Y-%m-%d")

    combinedData = callsForServiceData.set_index("occ_date").join(weatherData.set_index("DATE"), how="inner")
    combinedData.index.name = "Date"
    return combinedData
