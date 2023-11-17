import pandas as pd
import DataLoader

def __printOptions():
    print('')
    print("Processing Options:")
    print("0 - Exit")
    print("1 - Raw Data Processor")
    print('')

def getInput():
    return input("Process Number: ")

if (__name__ == "__main__"):
    userInput:str = None
    rawData:pd.DataFrame = None

    while (userInput != '0'):
        __printOptions()
        userInput = getInput()

        if (userInput == '1'):
            rawData = DataLoader.ProcessRawData()
        else:
            print("Unrecognized input. Please enter a single digit for the process # you would like to begin.")
