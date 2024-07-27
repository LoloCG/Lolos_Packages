import numpy as np
import pandas as pd

def interpolate_and_average_series(dataframe, X_column, Y_column):
    '''
    Combines multiple series data, interpolating Y for a common set of X values, and calculating the averages of the interpolated Y values.

    Parameters:
    dataframe (dict): A dictionary where keys are series names and values are DataFrames containing the series data.
    X_column (str): The name of the column in the DataFrames representing the X values.
    Y_column (str): The name of the column in the DataFrames representing the Y values.

    Returns:
    pandas.DataFrame: A DataFrame containing the common X values and the average interpolated Y values.

    Example use: 
        data = {
            'Series1': pd.DataFrame({'X': [1, 3, 5], 'Y': [10, 15, 20]}),
            'Series2': pd.DataFrame({'X': [2, 4, 6], 'Y': [12, 18, 24]})
        }
        result = interpolate_series(data, 'X', 'Y')
        data['Averages'] = result
        print(data)
    '''
    combined_X = np.array([])
    for series_name, df in dataframe.items():
        combined_X = np.union1d(combined_X, df[X_column]) # Combine and sort unique X values from all series

    # Creates a combined df with all unique X values and sorts them reseting the index
    df_combined = pd.DataFrame(combined_X, columns=[X_column])
    df_combined = df_combined.sort_values(by=X_column).reset_index(drop=True)

    # Interpolates Y values for each series at the combined X values, and adds them to the combined DataFrame with series-specific column names
    for series_name, df in dataframe.items():
        df_combined[f'{Y_column}_{series_name}'] = np.interp(df_combined[X_column], df[X_column], df[Y_column])

    # Calculates the average of interpolated Y values, storing them in a new column
    combined_Y_columns = [col for col in df_combined.columns if col.startswith(f'{Y_column}_')] # Identify all columns in the combined DataFrame that contain interpolated Y values
    df_combined[f'{Y_column}_avg'] = df_combined[combined_Y_columns].mean(axis=1)

    # Creates a DataFrame containing only the average interpolated Y values and the combined X values
    df_averages = df_combined[[f'{Y_column}_avg', X_column]]
    
    return df_averages

