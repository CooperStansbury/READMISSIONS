import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def build_fig(title="", axis_off=False, size=(5, 5), 
              y_lab="", x_lab="", title_size=15, dpi=300):
    """A function to build a matplotlib figure. Primary
    goal is to sandardize the easy stuff.
    Args:
        - title (str): the title of the plot
        - axis_off (bool): should the axis be printed?
        - size (tuple): how big should the plot be?
        - y_lab (str): y axis label
        - x_lab (str): x axis label
    Returns:
        fig (plt.figure)
    """
    fig = plt.figure(figsize=size, 
                     facecolor='w',
                     dpi=dpi)
    fig.suptitle(title, fontsize=title_size)
    plt.xlabel(x_lab, fontsize=title_size)
    plt.ylabel(y_lab, fontsize=title_size)
    
    if axis_off:
        plt.axis('off')
    return fig