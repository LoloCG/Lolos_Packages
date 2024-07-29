import pandas as pd

def find_closest_value(data, column, target):
    '''
    Returns the number that is closest to the target by absolute values from a selected column of a dataframe or dictionary structure.
    Also called "Simple K-Nearest Neighbors", "nearest neighbor search" or "proximity search". 
    
    Parameters:
    data (pd.DataFrame, dictionary, or list): The data structure containing the data.
    column (str): The name of the column to search.
    target (int or float): The target value to find the closest to.

    Returns:
    int or float: The closest value in the column to the target value.
    '''
    # Handle different data structures
    if isinstance(data, pd.DataFrame):
        df = data
    elif isinstance(data, dict):
        df = pd.DataFrame(data)
    elif isinstance(data, list):
        df = pd.DataFrame(data)
        column = 0
    else:
        raise ValueError("The input data must be a pandas DataFrame, dictionary, or list")

    closest_value = df[column].iloc[(df[column] - target).abs().argsort()[0]]
    return closest_value

    '''
    1- calculates the difference between each value in the column and the target.
    2- converts into absolute, which is equal to its proximity
    3- sorts the absolute differences
    4- returns the index 0 of the sorted differences, which is the closest.
    5- retrieves the actual value in the df
    '''