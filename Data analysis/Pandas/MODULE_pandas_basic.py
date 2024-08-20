import pandas as pd
import os

class DataCleaner:
    def __init__(self, dataframe: pd.DataFrame):
        self.dataframe = dataframe

    def convert_dataframe_dates(self, dateColumn, removeDateCol=False):
    
        print("Converting dataframe dates into datatime type...")
        #DEBUG: print("DataFrame columns before conversion:", list(self.dataframe.columns))
        
        #if 'Start Date' not in self.dataframe.columns:
        #    raise KeyError("The DataFrame does not contain a 'Start Date' column.")
        
        df = self.dataframe

        df['date'] = pd.to_datetime(df['Start Date'])
        # Extract year, month, and day 
        df['year'] = df['date'].dt.year 
        df['month'] = df['date'].dt.month 
        df['day'] = df['date'].dt.day

        if removeDateCol:
            df.drop('Start Date', axis=1,inplace=True)

        self.dataframe = df

    def normalize_strings(self, columnName):
        df = self.dataframe
        df[columnName] = df[columnName].str.strip().str.lower()
        self.dataframe = df
    
    def convert_comma_to_dot(self, columnName=None, replaceWhat = None, replaceWith = None):
        df = self.dataframe

        if replaceWhat is None and replaceWith is None:
            replaceWhat = ','
            replaceWith = '.'
        elif replaceWhat is ',':
            replaceWith = '.' #TODO: make this more dynamic... somehow...

        print(f"Replacing '{replaceWhat}' with '{replaceWith}' in column {columnName}")

        try:
            # Check if columnName is None or invalid
            if columnName is None:
                raise ValueError("Column name cannot be None.")
            
            if columnName not in df.columns:
                raise KeyError(f"Column '{columnName}' does not exist in the DataFrame.")
            
            # Perform the replacement operation
            df[columnName] = df[columnName].str.replace(replaceWhat, replaceWith).astype(float)

        except Exception as e:
            # Catch all other exceptions
            print(f"An unexpected error occurred: {e}")
            raise
            
        self.dataframe = df

    def split_column_multiple(self, columnName, separator, newColList, separatorNum = None, expand = True):
        df = self.dataframe
        print(f"Splitting column '{columnName}' into '{list(newColList)}'...")
        if separatorNum is None:
            separatorNum = 2

        df[newColList] = df[columnName].str.split(separator, n=separatorNum, expand=expand)
        self.dataframe = df

    def show_missing_files(self):
        df_raw = self.dataframe
        if df_raw.isnull().any().any():
            empty_columns = df_raw.columns[df_raw.isnull().any()]

            if len(empty_columns) > 0:
                print(f"Columns that have empty values: ")
                for column in empty_columns:
                    empty_values = df_raw[column].isnull().sum()
                    print(f"\t'{column}', with {empty_values}")

                    if empty_values == len(df_raw):
                        print(f"column '{column}' is completely empty ")
        else:
            print("No missing values in the dataset.")

class DataFrameTransformer:
    def __init__(self, dataframe: pd.DataFrame):
        self.dataframe = dataframe

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

# ============== UNUSED CODE ==================
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
