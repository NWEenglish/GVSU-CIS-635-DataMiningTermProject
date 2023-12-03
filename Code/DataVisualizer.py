import matplotlib.pyplot as plt
import pandas as pd
from sklearn import tree

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

def DecisionTree(columns:[str], model:tree.DecisionTreeClassifier) -> None:
    print("Graphing the decision tree...")

    plt.figure(figsize=(20, 10))
    tree.plot_tree(model, feature_names=columns, class_names=model.classes_, filled=True, rounded=True)
    plt.show()