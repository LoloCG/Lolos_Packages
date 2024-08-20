import pandas as pd
import os

class DataCleaner:
    def __init__(self, dataframe: pd.DataFrame):
        self.dataframe = dataframe

    def convert_dataframe_dates(self, removeDateCol=False):
        '''
        Converts a dataframe with unformatted dates into the datetime type of pandas.

        Parameters
            df (DataFrame), the raw dataframe without formatted datetime date variables.
            removeDateCol (bool), wether to keep (False) or delete (True) the old column of dates. Default false.
        '''
        print("Converting dataframe dates into datatime type...")
        #DEBUG: print("DataFrame columns before conversion:", list(self.dataframe.columns))
        
        if 'Start Date' not in self.dataframe.columns:
            raise KeyError("The DataFrame does not contain a 'Start Date' column.")
        
        df = self.dataframe

        df['date'] = pd.to_datetime(df['Start Date'])
        # Extract year, month, and day 
        df['year'] = df['date'].dt.year 
        df['month'] = df['date'].dt.month 
        df['day'] = df['date'].dt.day

        if removeDateCol:
            df.drop('Start Date', axis=1,inplace=True)

        self.dataframe = df

    def basic_raw_pretreatment(self):
        '''
        Does a basic precleaning of the dataset required for most typical functions required for analyzing academic study hours

        Parameters
            df_raw (DataFrame), the raw dataframe without pre-treatment

        Returns
            df_clean (DataFrame)
        '''
        print("Doing data pre-treatment...")
        last_column = 'Path'
        df_raw = self.dataframe

        # Splits the last column into 3, adds them into df_raw  
        df_raw[['Period', 'Subject', 'Path3']] = df_raw[last_column].str.split('\\', n=2, expand=True)

        df_raw['Time Spent (Hrs)'] = df_raw['Time Spent (Hrs)'].str.replace(',', '.').astype(float) # Replaces commas with dots and convert to numeric the column of time spent
        
        df_raw['Subject'] = df_raw['Subject'].str.strip().str.lower() # Normalize the subject names

        # print(f"Pre-cleaned data:\n{df_clean.head(3)}")
        
        self.dataframe = df_raw

    def show_missing_files(self):
        df_raw = self.dataframe
        if df_raw.isnull().any().any():
            empty_columns = df_raw.columns[df_raw.isnull().any()]

            if len(empty_columns) > 0:
                print(f"\nColumns that have empty values: ")
                for column in empty_columns:
                    empty_values = df_raw[column].isnull().sum()
                    # empty_values = df_raw[column[df_raw.isnull().sum()]]
                    print(f"- '{column}', with {empty_values}")

                    if empty_values == len(df_raw):
                        print(f"column '{column}' is completely empty ")
        else:
            print("No missing values in the dataset.")

class DataFrameTransformer:
    def __init__(self, dataframe: pd.DataFrame):
        self.dataframe = dataframe
        print()

    def pivot_dataframe(self):
        df = self.dataframe
        # (index='indexCol', columns='columns', values='valueColumns')

        self.dataframe = df

    def filter_df_column_by_val(self,ColToFilter,FilterValues):
        print(f"Filtering dataframe for values {list(FilterValues)} located in column '{ColToFilter}'...")

        df = self.dataframe
        df = df[df[ColToFilter].isin(FilterValues)]
        self.dataframe = df
    
    def multiIndex_group(self, colsToGroup):
        '''
        From a dataframe of 3 columns, groups the numerical values by 
            two categorical value columns of a dataframe, returning an index-reset dataframe
        
        Parameters:
            df (dataframe), that is pre-processed. It can include other columns that 
                are not going to be grouped, as the function will only select those that will.
            
            colsToGroup (list), must include 3 column names as string which must be in the following order:
                numerical data, greater categorical data, lower categorical data.
        '''
        print(f"Grouping {colsToGroup[0]} by {colsToGroup[1]} and {colsToGroup[2]}...")

        df = self.dataframe
        df = df[colsToGroup]
        df = df.groupby([colsToGroup[1],colsToGroup[2]]).sum().reset_index()

        self.dataframe = df


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

def group_numCol_by_catCol(df, num_var, cat_var=None): 
    '''
    Used to group numeric variable column by a categorical one.

    Parameters:
        df (DataFrame), The one that contains all the pre-cleaned data. Does not require it to contain the only two columns, and can be given entirely
        num_var (str), the name of the column with the numerical data
        cat_var (str), the name of the column with the categorical data
        
    Returns:
        Grouped (DataFrameGroupBy type object), that consists on two columns of all numerical grouped by the categoricals
    '''
    df_group = df[[cat_var, num_var]] 
    print(f"grouping {num_var} by {cat_var}")
    grouped = df_group.groupby(cat_var)

    return grouped

def multiIndex_group_sum(df, colsToGroup):
    '''
    From a dataframe of 3 columns, groups the numerical values by 
        two categorical value columns of a dataframe, returning an index-reset dataframe
    
    Parameters:
        df (dataframe), that is pre-processed. It can include other columns that 
            are not going to be grouped, as the function will only select those that will.
        
        colsToGroup (list), must include 3 column names as string which must be in the following order:
            numerical data, greater categorical data, lower categorical data.
    '''
    df_group = df[[colsToGroup[0], colsToGroup[1], colsToGroup[2]]]

    print(f"Grouping {colsToGroup[0]} by {colsToGroup[1]} and {colsToGroup[2]}")
    
    multiGroup_sum = df_group.groupby([colsToGroup[1],colsToGroup[2]]).sum()

    indx_multiGroup_sum = multiGroup_sum.reset_index()

    return indx_multiGroup_sum