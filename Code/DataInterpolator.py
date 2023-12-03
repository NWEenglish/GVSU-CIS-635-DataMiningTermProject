import pandas as pd

def InterpolateCallsForServiceData(callsForServiceData:pd.DataFrame) -> pd.DataFrame:
    print("Beginning the process of interpolating the Calls-for-Service data...")

    retData = callsForServiceData.copy()

    # All unique dates and case types
    allDates = retData['occ_date'].unique()
    allCaseTypes = retData['CASE DESC'].unique()

    # Ensure every combination of dates and case types have a value (default 0)
    all_combinations = pd.DataFrame([(date, case_desc) for date in allDates for case_desc in allCaseTypes], columns=['occ_date', 'CASE DESC'])

    # Merge to fill in missing values with 0
    retData = pd.merge(all_combinations, retData, on=['occ_date', 'CASE DESC'], how='left').fillna(0)

    return retData

def InterpolateWeatherData(weatherData:pd.DataFrame) -> pd.DataFrame:
    print("Beginning the process of interpolating the Weather data...")

    retData = weatherData.copy()

    # TAVG - Average of hourly values - The weather station didn't start recording this until April 1, 2013. We'll assume it's the 
    # average of the max and min temp for that day.
    retData["TAVG"] = retData[["TMAX", "TMIN"]].mean(axis = 1).interpolate()

    # WT** are flags for weather types. Value 1 represents that a given weather type was observed, but no value does not necessarily mean
    # the absence. However, for the purposes of this project, we will assume it not being observed means it did not happen.
    wtFlags = ["WT01", "WT02", "WT03", "WT04", "WT05", "WT06", "WT08", "WT09", "WT10", "WT13", "WT14", "WT16", "WT18", "WT21", "WT22"]
    for flag in wtFlags:
        retData[flag].fillna(0, inplace = True)

    return retData
