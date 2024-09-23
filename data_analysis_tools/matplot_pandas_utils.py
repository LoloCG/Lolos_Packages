import matplotlib.pyplot as plt
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


# ========================= MODULE_matplot_pandas/DataPlotter =========================
# =================================== 2024/02/09 =========================

class DataPlotter:
    def __init__(self, dataframe: pd.DataFrame):
        self.dataframe = dataframe

        self.categorical_columns = None
        self.numerical_columns = None
        self.highest_hierarchy_column = None

        print()

    def identify_column_hierarchy(self):
        df = self.dataframe
        cat_cols = []
        Num_col = None
        num_uniq_val = 0
        first_hier_col = None

        for colname in df:
            coltype = str(df[colname].dtype)
            if coltype == 'object': 
                cat_cols.append(colname)

                if df[colname].value_counts().mean() > num_uniq_val:
                    
                    num_uniq_val = df[colname].value_counts().mean()
                    first_hier_col = colname

            elif coltype in ['float64','int64']:
                Num_col = colname

        #print(f"Category columns: {list(cat_cols)}")
        #print(f"Numerical columns: {Num_col}")
        print(f"Categorical columm with highest hierarchy: {first_hier_col}")
        #categ_in_highest_hierarch = list(df[first_hier_col].unique())
        #print(f"Categories: {categ_in_highest_hierarch[0]}, {categ_in_highest_hierarch[1]}")

        self.highest_hierarchy_column = first_hier_col        
        self.categorical_columns = cat_cols
        self.numerical_columns = Num_col

    def plot_stacked_bar_chart(self):
        print()
        clean_dataframe.plot(kind='bar', stacked=True, figsize=(10, 6))

        plt.title('Weekly Hours Spent on Subjects')
        plt.xlabel('Week')
        plt.ylabel('Time Spent (Hrs)')
        plt.legend(title='Subject')
        plt.xticks(rotation=45)
        plt.tight_layout()

        plt.show()

    def plot_hierarchical_categorical_bar_chart(self):
        """
        Plots a bar chart using a DataFrame with two categorical columns and one numerical column,
        where one categorical column represents a higher hierarchy.

        Parameters:
        df (pd.DataFrame): DataFrame containing the data to plot. It should contain two categorical columns 
                        (one representing a higher hierarchy) and one numerical column.
        """
        # This is to be replaced later by a list parameter in the function...
        catCol1 = self.highest_hierarchy_column 
        catCol2 = list(set(self.categorical_columns) - {catCol1})[0]
        numCol = self.numerical_columns

        df = self.dataframe

        periods = df[catCol1].unique()

        print(f"Plotting bar chart of {numCol} per {catCol2}, separated by {catCol1}...")

        x_values_dict = {period: [] for period in periods}    # Initialize lists to store x values for each period

        fig, ax = plt.subplots(figsize=(10, 6))

        n = 1
        for period in periods:
            filt_df = df[df[catCol1] == period]  

            for subject in filt_df[catCol2]:
                # DEBUG: print(f"{n} - period: {period}, Subject: {subject}") 
                x_values_dict[period].append(n)
                n += 1

            x_values = x_values_dict[period]
            y_values = df.loc[df[catCol1] == period, numCol]
            ax.bar(x_values, y_values, width=0.8, label=period, align='center')

        # Customizing the x-ticks to match the subjects
        all_subjects = list(df[catCol2])
        ax.set_xticks(range(1, n))
        ax.set_xticklabels(all_subjects, rotation=45)

        ax.legend(title=catCol1)
        ax.set_xlabel(catCol2)
        ax.set_ylabel(numCol)
        chartTitle = numCol + " per " + catCol2
        plt.legend(title=chartTitle)
        plt.xticks(rotation=45)
        plt.tight_layout() 
        plt.show()
