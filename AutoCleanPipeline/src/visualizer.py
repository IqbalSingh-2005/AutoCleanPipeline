import pandas as pd
import matplotlib.pyplot as plt

def visual(df: pd.DataFrame):
    fig, ax = plt.subplots()

    x = df[df.columns[0]]
    y = df[df.columns[1]]

    ax.plot(x,y)
    plt.show()



  