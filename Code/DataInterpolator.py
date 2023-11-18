import pandas as pd

def InterpolateData(weatherData:pd.DataFrame) -> pd.DataFrame:
    print("Beginning the process of interpolating the data...")

    interpolatedData = __weatherDataInterpolation(weatherData)

    print("Completed the process of interpolating the data.")

    return interpolatedData

def __weatherDataInterpolation(weatherData:pd.DataFrame) -> pd.DataFrame:
    print("Interpolating weather data...")

    retData = weatherData.copy()

    return retData