import pandas as pd

def InterpolateData(weatherData:pd.DataFrame) -> pd.DataFrame:
    print("Beginning the process of interpolating the data...")

    interpolatedData = __weatherDataInterpolation(weatherData)

    print("Completed the process of interpolating the data.")

    return interpolatedData

def __weatherDataInterpolation(weatherData:pd.DataFrame) -> pd.DataFrame:
    print("Interpolating weather data...")

    retData = weatherData.copy()

    # Below are all the fields that have missing weather data for, with a description of how we will resolve them.

    # TAVG - Average of hourly values - The weather station didn't start recording this until April 1, 2013. We'll assume it's the 
    # average of the max and min temp for that day.
    retData["TAVG"] = retData[["TMAX", "TMIN"]].mean(axis = 1).interpolate()

    # WDF5 - Direction of fastest 5-second wind (degrees) - We'll assume it wouldn've been similar to the fastest 2-minute wind speed and so
    # we will use the same value for that day.
    retData["WDF5"] = retData["WDF2"].interpolate()

    # WSF5 - Fastest 5-second wind speed (mph) - We'll assume it would have been at least the same as the fastest 2-min wind speed for that 
    # day since that would've been at least the minimum value for the 5-second, but we can't possibly know the highest it could've been.
    retData["WSF5"] = retData["WSF2"].interpolate()

    # WT** are flags for weather types. Value 1 represents that a given weather type was observed, but no value does not necessarily mean
    # the absence. However, for the purposes of this project, we will assume it not being observed means it did not happen.
    wtFlags = ["WT01", "WT02", "WT03", "WT04", "WT05", "WT06", "WT08", "WT09", "WT10", "WT13", "WT14", "WT16", "WT18", "WT21", "WT22"]
    for flag in wtFlags:
        retData[flag].fillna(0, inplace = True)

    return retData
