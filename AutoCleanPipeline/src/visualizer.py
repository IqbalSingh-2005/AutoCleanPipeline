import pandas as pd
import matplotlib.pyplot as plt

def visual(df: pd.DataFrame):

    x = df[df.columns[0]]
    y = df[df.columns[1]]

    fig, axes = plt.subplots(3, 1, figsize=(8, 12))

    # Line plot
    axes[0].plot(x, y)
    axes[0].set_title("Line Plot")

    # Scatter plot
    axes[1].scatter(x, y)
    axes[1].set_title("Scatter Plot")

    # Bar plot
    axes[2].bar(x, y)
    axes[2].set_title("Bar Plot")

    plt.tight_layout()
    plt.show()