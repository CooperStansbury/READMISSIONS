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


def rand_jitter(arr, factor=.01):
    stdev = factor * (max(arr) - min(arr))
    return arr + np.random.randn(len(arr)) * stdev


def load_col_names():
    """ function to load a dict of column names"""
    COLUMNS = {}
    tmp = pd.read_csv("../cleaned_data/population_column_map.csv")
    COLUMNS['POPULATION'] = dict(zip(tmp.GEO_ID, tmp.id))

    tmp = pd.read_csv("../cleaned_data/income_column_map.csv")
    COLUMNS['INCOME'] = dict(zip(tmp.GEO_ID, tmp.id))

    tmp = pd.read_csv("../cleaned_data/occuptation_column_map.csv")
    COLUMNS['OCCUPTATION'] = dict(zip(tmp.GEO_ID, tmp.id))

    tmp = pd.read_csv("../cleaned_data/education_column_map.csv")
    COLUMNS['EDUCATION'] = dict(zip(tmp.GEO_ID, tmp.id))

    tmp = pd.read_csv("../cleaned_data/eigenvalue_column_map.csv")
    COLUMNS['RED_EIGENVALUES'] = tmp['Red_Columns'].to_list()
    COLUMNS['GREEN_EIGENVALUES'] = tmp['Green_Columns'].to_list()
    COLUMNS['BLUE_EIGENVALUES'] = tmp['Blue_Columns'].to_list()

    tmp = pd.read_csv("../cleaned_data/landuse_column_map.csv")
    COLUMNS['LANDUSE'] = tmp['Land_Use_Column_Name'].to_list()

    tmp = pd.read_csv("../cleaned_data/google_column_map.csv")
    COLUMNS['GOOGLE_REDS'] = [x for x in tmp['r_color_pixel_columns'] if str(x) != 'nan']
    COLUMNS['GOOGLE_GREENS']  = [x for x in tmp['g_color_pixel_columns'] if str(x) != 'nan']
    COLUMNS['GOOGLE_BLUES'] = [x for x in tmp['b_color_pixel_columns'] if str(x) != 'nan']
    COLUMNS['GOOGLE_COLOR_SCORES'] = [x for x in tmp['color_score_columns'] if str(x) != 'nan']
    COLUMNS['GOOGLE_COLOR_FRACTIONS'] = [x for x in tmp['color_fraction_columns'] if str(x) != 'nan']
    COLUMNS['GOOGLE_LABELS'] = [x for x in tmp['Label_columns'] if str(x) != 'nan']
    COLUMNS['GOOGLE_LABEL_SCORES'] = [x for x in tmp['Label_score_columns'] if str(x) != 'nan']
    COLUMNS['GOOGLE_MANUAL_LABELS'] = [x.strip() for x in open("../image_data/manual_labels.txt")]

    return COLUMNS
    