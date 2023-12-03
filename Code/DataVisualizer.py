import matplotlib.pyplot as plt
import pandas as pd

def GraphData(data:pd.DataFrame, caseType:str) -> None:
    print("Graphing the data...")

    graphData = data[data['CASE DESC'] == caseType]
    plt.figure(figsize=(10, 6))
    plt.plot(graphData['Date'], graphData['Count Category'], marker='o', linestyle='-', color='b')
    plt.title(f'Daily Trend for {caseType}')
    plt.xlabel('Date')
    plt.ylabel('Count')
    plt.grid(True)
    plt.show()