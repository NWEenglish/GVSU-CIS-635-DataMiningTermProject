import pandas as pd
import os
import GlobalConfigs

def ImportRawData() -> dict[str, pd.DataFrame]:
    print("Beginning the process of importing raw data...")

    rawData = dict(callsForService = __processCallsForServiceData(), weather = __processWeatherData())

    print("Completed the process of importing raw data.")

    return rawData

def ImportCleanData() -> pd.DataFrame:
    print("Beginning the process of importing clean data...")
    cleanData = pd.read_csv(GlobalConfigs.CLEANED_DATA_FILEPATH).set_index('Date')
    print("Completed the process of importing clean data.")

    return cleanData

def ImportNormalizedData() -> pd.DataFrame:
    print("Beginning the process of importing normalized data...")
    normalizedData = pd.read_csv(GlobalConfigs.NORMALIZED_DATA_FILEPATH).set_index('Date')
    print("Completed the process of importing normalized data.")

    return normalizedData

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
