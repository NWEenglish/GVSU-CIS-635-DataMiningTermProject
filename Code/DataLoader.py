import pandas as pd
import os

RAW_DATA_FOLDER = "./Raw Data/"
CLEAN_DATA_FOLDER = "./Clean Data/"

def ProcessRawData() -> pd.DataFrame:
    print("Beginning the processing of raw data...")

    cfsData = __processCallsForServiceData()
    wData = __processWeatherData()
    joinedData = __joinDataTables(cfsData, wData)

    print("Completed the processing of raw data.")

    return joinedData

def __processCallsForServiceData() -> pd.DataFrame:
    print("Reading in Calls-for-Service data...")

    data = pd.DataFrame()

    for file in os.listdir(RAW_DATA_FOLDER):
        if file.startswith("NIJ"):
            data = pd.concat([data, pd.read_csv(RAW_DATA_FOLDER + file)])

    return data

def __processWeatherData() -> pd.DataFrame:
    print("Reading in Weather data...")
    data = pd.read_csv(RAW_DATA_FOLDER + "NOAA_Weather.csv")
    return data

def __joinDataTables(callsForServiceData:pd.DataFrame, weatherData:pd.DataFrame):
    print("Merging data...")

    # Convert dates in data frames to a consistent format
    callsForServiceData['occ_date'] = pd.to_datetime(callsForServiceData['occ_date'], format='%m/%d/%Y')
    weatherData['DATE'] = pd.to_datetime(weatherData['DATE'], format='%Y-%m-%d')

    combinedData = callsForServiceData.set_index("occ_date").join(weatherData.set_index("DATE"), how='inner')
    return combinedData
