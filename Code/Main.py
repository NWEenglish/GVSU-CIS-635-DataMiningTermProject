import pandas as pd
import DataLoader
import DataCleaner
import DataLearning
import DataNormalizer

def __printOptions():
    print('')
    print("Processing Options:")
    print("0 - Exit")
    print("1 - Import Raw Data")
    print("2 - Bin, Clean, Interpolate, and Save Raw Data")
    print("3 - Import Cleaned Data")
    print("4 - Normalize and Save Cleaned Data") 
    print("5 - Import Normalized Data")
    print("6 - Learn and Test KNN and Decision Trees models")
    print("7 - Graph KNN and Decision Trees models")
    print("8 - Perform Correlation Analysis (x^2)")
    print('')

def getInput():
    return input("Process Number: ")

if (__name__ == "__main__"):
    userInput:str = None
    rawData = {}
    cleanData = pd.DataFrame()
    normalizedData = pd.DataFrame()
    learnedData = {}

    while (True):
        __printOptions()
        userInput = getInput()

        # Exit processing
        if (userInput == '0'):
            break

        # Imports raw data
        elif (userInput == '1'):
            rawData = DataLoader.ImportRawData()

        # Bin, clean, interpolate, combine, and save the data
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

        # Learn and TestKNN and Decision Tree models
        elif (userInput == '6'):
            if (normalizedData.empty):
                print("No normalized data has been previously loaded.")
            else :
                learnedData = DataLearning.LearnAndTest(normalizedData)

        # Graph KNN and Decision Tree models
        elif (userInput == '7'):
            if (not learnedData):
                print("No data has been previously learned.")
            else :
                DataLearning.Graph(learnedData)

        # Perform Correlation Analysis (x^2)
        elif (userInput == '8'):
            if (normalizedData.empty):
                print("No normalized data has been previously loaded.")
            else :
                DataLearning.CorrelationAnalysis(normalizedData)

        # Unknown input
        else:
            print("Unrecognized input. Please enter a single digit for the process # you would like to begin.")
