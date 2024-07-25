"""
This script generates a scatter plot with interpolated data from three different series.
It calculates the average of the interpolated Y values and plots this average along with the individual series.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def main():
    # Sample data for three series in dictionary form
    data_dict = {
        'Series1': {'X': [1, 3, 5, 7], 'Y': [10, 15, 20, 25]},
        'Series2': {'X': [2, 4, 6, 8, 10], 'Y': [12, 18, 24, 30, 31]},
        'Series3': {'X': [1, 2, 3, 4, 5], 'Y': [14, 16, 18, 20, 22]}
    }

    # Create DataFrames for each series
    df_dict = create_df_dict(data_dict)

    # Interpolate and combine data from all series
    df_combined = interpolate_data_dictionary(df_dict)
    print(df_combined)
    
    # Plot the combined and interpolated data
    plot_chart(df_combined)

def plot_chart(df_combined):
    """
    Plots the combined data with interpolated Y values and their average.
    """
    print("Plotting chart")

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(df_combined['X'], df_combined['Y1'], label='Series1', marker='o')
    plt.plot(df_combined['X'], df_combined['Y2'], label='Series2', marker='x')
    plt.plot(df_combined['X'], df_combined['Y3'], label='Series3', marker='s')
    plt.plot(df_combined['X'], df_combined['Y_avg'], label='Average', linestyle='--', color='black')

    # Adding labels and legend
    plt.xlabel('X (mm of travel)')
    plt.ylabel('Y (kN of force)')
    plt.title('Interpolated and Averaged Series Data')
    plt.legend()
    plt.grid(True)

    # Show the plot
    plt.show()

def create_df_dict(data_dict):
    """
    Converts the data dictionary into a dictionary of DataFrames.
    
    Parameters:
    data_dict (dict): A dictionary containing data for multiple series.
    
    Returns:
    dict: A dictionary where keys are series names and values are DataFrames.
    """
    df_dict = {}
    for series_name, series_data in data_dict.items():
        print(f"Loading: {series_name}")
        df_dict[series_name] = pd.DataFrame(series_data)
    return df_dict

def interpolate_data_dictionary(df_dict):
    """
    Interpolates the Y values for each series at all unique X values and calculates the average Y value.
    
    Parameters:
    df_dict (dict): A dictionary of DataFrames for each series.
    
    Returns:
    DataFrame: A combined DataFrame with interpolated Y values and their average.
    """
    print()

    # Combine all unique X values from all series
    combined_X = np.union1d(np.union1d(df_dict['Series1']['X'], df_dict['Series2']['X']), df_dict['Series3']['X'])

    # Create a combined DataFrame with all unique X values
    df_combined = pd.DataFrame(combined_X, columns=['X'])
    df_combined = df_combined.sort_values(by='X').reset_index(drop=True)

    # Interpolate Y values for each series at the combined X values
    df_combined['Y1'] = np.interp(df_combined['X'], df_dict['Series1']['X'], df_dict['Series1']['Y'])
    df_combined['Y2'] = np.interp(df_combined['X'], df_dict['Series2']['X'], df_dict['Series2']['Y'])
    df_combined['Y3'] = np.interp(df_combined['X'], df_dict['Series3']['X'], df_dict['Series3']['Y'])

    # Calculate the average of Y values
    df_combined['Y_avg'] = df_combined[['Y1', 'Y2', 'Y3']].mean(axis=1)

    return df_combined

# Run the main function
main()

