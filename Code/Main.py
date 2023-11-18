import pandas as pd
import DataLoader
import DataCleaner
import DataNormalizer

def __printOptions():
    print('')
    print("Processing Options:")
    print("0 - Exit")
    print("1 - Import Raw Data")
    print("2 - Clean, Interpolate, and Save Raw Data")
    print("3 - Import Cleaned Data")
    print("4 - Normalize and Save Cleaned Data") 
    print("5 - Import Normalized Data")
    print('')

def getInput():
    return input("Process Number: ")

if (__name__ == "__main__"):
    userInput:str = None
    rawData = dict[str, pd.DataFrame]
    cleanData = pd.DataFrame()
    normalizedData = pd.DataFrame()

    while (True):
        __printOptions()
        userInput = getInput()

        # Exit processing
        if (userInput == '0'):
            break

        # Imports raw data
        elif (userInput == '1'):
            rawData = DataLoader.ImportRawData()

        # Clean, interpolate, combine, and save data
        elif (userInput == '2'):
            if (not rawData or any(df.empty for df in rawData.values())):
                print("No raw data has been previously loaded.")
            else:
                cleanData = DataCleaner.CleanData(rawData)

        # Import clean data
        elif (userInput == '3'):
            cleanData = DataLoader.ImportCleanData()

        # Normalize and save cleaned data
        elif (userInput == '4'):
            if (cleanData.empty):
                print("No cleaned data has been previously loaded.")
            else:
                normalizedData = DataNormalizer.NormalizeData(cleanData)

        # Import normalized data
        elif (userInput == '5'):
            normalizedData = DataLoader.ImportNormalizedData()

        # Unknown input
        else:
            print("Unrecognized input. Please enter a single digit for the process # you would like to begin.")
