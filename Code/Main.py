import pandas as pd
import DataLoader
import DataCleaner
import DataInterpolatorAndNormalizer

def __printOptions():
    print('')
    print("Processing Options:")
    print("0 - Exit")
    print("1 - Import Raw Data")
    print("2 - Clean and Save Raw Data")
    print("3 - Import Cleaned Data")
    print("4 - Interpolate, Normalize, and Save Cleaned Data")
    print("5 - Import Normalized Data")
    print('')

def getInput():
    return input("Process Number: ")

if (__name__ == "__main__"):
    userInput:str = None
    rawData = pd.DataFrame()
    cleanData = pd.DataFrame()
    normalizedData = pd.DataFrame()

    while (userInput != '0'):
        __printOptions()
        userInput = getInput()

        # Imports raw data
        if (userInput == '1'):
            rawData = DataLoader.ImportRawData()

        # Clean and save data
        elif (userInput == '2'):
            if (rawData.empty):
                print("No raw data has been previously loaded.")
            else:
                cleanData = DataCleaner.CleanData(rawData)

        # Import clean data
        elif (userInput == '3'):
            cleanData = DataLoader.ImportCleanData()

        # Interpolate, normalize, and save cleaned data
        elif (userInput == '4'):
            if (cleanData.empty):
                print("No cleaned data has been previously loaded.")
            else:
                normalizedData = DataInterpolatorAndNormalizer.InterpolateAndNormalizeData(cleanData)

        # Import normalized data
        elif (userInput == '5'):
            normalizedData = DataLoader.ImportNormalizedData()

        # Unknown input
        else:
            print("Unrecognized input. Please enter a single digit for the process # you would like to begin.")
