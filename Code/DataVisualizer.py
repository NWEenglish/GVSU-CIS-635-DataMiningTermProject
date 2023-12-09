import GlobalConfigs
import matplotlib.pyplot as plt
import pandas as pd
from sklearn import tree

def DecisionTree(columns:[str], model:tree.DecisionTreeClassifier, caseType:str) -> None:
    print(f"Graphing the decision tree for '{caseType}'...")

    plt.figure(figsize=(40, 10))
    tree.plot_tree(model, feature_names=columns, class_names=model.classes_, filled=True, rounded=True)
    plt.suptitle(caseType, fontsize=40)
    plt.savefig(f'{GlobalConfigs.DECISION_TREE_GRAPHS_FILEPATH}{caseType}.png', dpi=600)
    plt.close()
