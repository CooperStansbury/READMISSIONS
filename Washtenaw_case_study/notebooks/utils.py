"""
Description:
    A collection of utiliy functions for reuse across 
    notebooks

Author:
    cstansbu
"""
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt



def build_fig(title="", axis_off=False, size=(5, 5), 
              y_lab="", x_lab="", title_size=12):
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
                     facecolor='w')
    fig.suptitle(title, fontsize=title_size)
    plt.xlabel(x_lab, fontsize=title_size)
    plt.ylabel(y_lab, fontsize=title_size)
    
    if axis_off:
        plt.axis('off')
    return fig