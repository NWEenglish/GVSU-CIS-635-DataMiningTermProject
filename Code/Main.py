import pandas as pd
import DataLoader
import DataCleaner

def __printOptions():
    print('')
    print("Processing Options:")
    print("0 - Exit")
    print("1 - Import Raw Data")
    print("2 - Clean and Save Raw Data")
    print("3 - Import Clean Data")
    print('')

def getInput():
    return input("Process Number: ")

if (__name__ == "__main__"):
    userInput:str = None
    rawData = pd.DataFrame()
    cleanData = pd.DataFrame()

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

        # Unknown input
        else:
            print("Unrecognized input. Please enter a single digit for the process # you would like to begin.")
