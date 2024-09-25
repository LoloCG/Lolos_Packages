import pandas as pd

class DFCleaner:
    def __init__(self, dataframe: pd.DataFrame):
        if not isinstance(dataframe, pd.DataFrame):
            raise TypeError("Expected input to be a pandas DataFrame.")
        else: self.dataframe = dataframe

    def column_exists(self, column):
        df = self.dataframe
        if column not in df.columns:
            raise KeyError(f"Column '{column}' not found in the DataFrame.")
        
        return

    def convert_df_dates(self, date_column, single_col=False):

        df = self.dataframe
        
        self.column_exists(date_column)

        if pd.api.types.is_datetime64_any_dtype(df[date_column]):
            # raise Exception(f"Column {date_column} is already datetime type...")
            print(f"Warning: Column {date_column} is already datetime type.")
            return self

        # TODO: add errorhandling for invalid date types

        df['date'] = pd.to_datetime(df[date_column])
        df.drop(date_column, axis=1, inplace=True)

        if not single_col:
            # TODO: add error handling to fill NaN rows
            df['year'] = df['date'].dt.year 
            df['month'] = df['date'].dt.month 
            df['day'] = df['date'].dt.day
            df.drop('date', axis=1, inplace=True)
        
        self.dataframe = df

        return self

    def convert_df_times(self, time_column, single_col=False, time_format='%H:%M'):
        '''
        Converts a column with time in HH:MM format into datetime or separate columns for hours and minutes.
        '''
        df = self.dataframe

        self.column_exists(time_column)
        
        if pd.api.types.is_datetime64_any_dtype(df[time_column]):
            print(f"Warning: Column {time_column} is already in datetime type.")
            return self

        # Ensure that the column contains strings and fill NaN values with a placeholder
        df[time_column] = df[time_column].fillna('')
        if not pd.api.types.is_string_dtype(df[time_column]):
            df[time_column] = df[time_column].astype(str)

        # errors='coerce' handles invalid formats by setting NaT
        df['time'] = pd.to_datetime(df[time_column], format=time_format, errors='coerce')
        df.drop(time_column, axis=1, inplace=True)
         
        if df['time'].isnull().any():
            print(f"Warning: Some values in column '{time_column}' could not be converted and are NaT.")

        if not single_col:
            df['hour'] = df['time'].dt.hour
            df['minute'] = df['time'].dt.minute
            df['second'] = df['time'].dt.second
            df.drop('time', axis=1, inplace=True)

        self.dataframe = df
        return self

    def replace_comma_to_dot(self, column):
        df = self.dataframe
        
        self.column_exists(column)

        if not pd.api.types.is_string_dtype(df[column]):
            raise TypeError(f"Expected a string column for {column}.")

        # df[column] = df[column].str.replace(',', '.').astype(float)

        df[column] = df[column].astype(str).str.replace(',', '.').astype(float)

        self.dataframe = df

        return self

    def normalize_column_strings(self, column, headers=True, items=True):
        df = self.dataframe
        self.column_exists(column)

        if items: df[column] = df[column].str.strip().str.lower().str.title()
        if headers: df.columns = df.columns.str.strip().str.lower().str.title()

        self.dataframe = df

        return self

    def split_column(self, column, separator, new_columns, expand=True, drop_old=True):
        '''
            Splits a column into multiple based on a separator.
        '''
        df = self.dataframe
        self.column_exists(column)
        
        if not pd.api.types.is_string_dtype(df[column]): # Validate if column is not str...
            df[column] = df[column].astype(str)

        df[column] = df[column].fillna('')  # Fill NaNs with empty strings before splitting

        n_separation = len(new_columns)-1
        df[new_columns] = df[column].str.split(separator, n=n_separation, expand=expand)

        if drop_old: df.drop(column, axis=1, inplace=True)
        
        self.dataframe = df
        return self
