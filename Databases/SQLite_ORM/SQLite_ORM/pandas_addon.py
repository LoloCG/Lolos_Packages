import pandas as pd
import sqlite3

def retrieve_all_data_as_df(self, tableName=None): # Still not tested
    if tableName is None and self.main_table_name is None:
        raise BaseException(f"Database table name and main table name are None.")
    elif tableName is None:
        print(f"DEBUG: table name is None when retrieving data...\ntable name used is {self.main_table_name}")
        tableName = self.main_table_name

    if self.connector is None or self.cursor is None:
        print(f"DEBUG: connector or cursor is None, creating connection to db")
        self.connector = sqlite3.connect(self.db_path)
        self.cursor = self.connector.cursor()
    else:
        print(f"DEBUG: Using existing connection and cursor")

    self.cursor.execute(f'SELECT * FROM {tableName}')

    # Fetch all rows
    rows = self.cursor.fetchall()
    
    # Get column names from the cursor
    column_names = [description[0] for description in self.cursor.description]
    
    import pandas as pd
    df = pd.DataFrame(rows, columns=column_names)
    
    return df

def insert_data_from_df(dataframe, connector_obj, table_name, if_exists='append', index=False):
    '''        
        if_exists (str): What to do if the table already exists ('fail', 'replace', 'append').
        index (bool): Whether to write the DataFrame index as a column.
    '''
    if not isinstance(dataframe, pd.DataFrame):
        raise TypeError(f"The variable passed to insert data to database is not dataframe type. It is '{type(dataframe)}'")

    connection = connector_obj.conn

    try:
        dataframe.to_sql(table_name, connection, if_exists=if_exists, index=index)
        connection.commit()

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        connection.rollback()

def insert_newdata_from_df(dataframe, connector_obj, table_name, unique_cols=None):
    '''
        unique_cols (list): The column(s) used to determine uniqueness in the table.
    '''
    pass
    if not isinstance(dataframe, pd.DataFrame):
        raise TypeError(f"The variable passed to insert data to database is not dataframe type. It is '{type(dataframe)}'")

    connection = connector_obj.conn
    
    where_clause = ''
    if unique_cols is not None: 
        where_clause = " WHERE " + " AND ".join([f'"{col}" = ?' for col in unique_cols])

    query = f"SELECT * FROM {table_name} {where_clause}"
    
    try:
        existing_data = pd.read_sql(
            sql=query,
            con=connection,
            params=tuple(dataframe[unique_cols].iloc[0]))

    except Exception as e:
        print(f"Error querying existing data: {e}")
        return
    
    if not existing_data.empty: # Filter out rows that already exist in the database
        dataframe_to_insert = dataframe.merge(existing_data, on=unique_cols, how='left', indicator=True)
        dataframe_to_insert = dataframe_to_insert[dataframe_to_insert['_merge'] == 'left_only'].drop(columns='_merge')
    else:
        dataframe_to_insert = dataframe
    if dataframe_to_insert.empty:
        print("No new data to insert.")
        return
        
    try:
        dataframe_to_insert.to_sql(
            table_name, 
            con=connection, 
            if_exists='append', 
            index=False)
        connection.commit()
        # print(f"Inserted {len(dataframe_to_insert)} new rows into {table_name}.")
    
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        connection.rollback()

def retrieve_columns_as_df(connector_obj, table_name, columns):
    '''
        Fetch specific columns from a SQLite table.
    '''
    connection = connector_obj.conn if connector_obj.conn else connector_obj.connect()

    columns_str = ", ".join(columns)
    query = f"SELECT {columns_str} FROM {table_name}"
    df = pd.read_sql_query(query, connection)
    return df

def retrieve_as_df(connector_obj, table_name, conditions=None):
    '''
    Retrieves data from a specified SQL table and returns it as a pandas DataFrame. 
        Allows for flexible querying with or without conditions
    Parameters:
        connector_obj: The database connector object that holds the connection to the database
        conditions (dict, optional): A dictionary where keys are column names and 
            values are the corresponding values to filter the data. 
            If a value is a list, it will be treated as an IN clause (e.g., WHERE column IN (...)).
    '''
    connection = connector_obj.conn if connector_obj.conn else connector_obj.connect()
    
    if not conditions:
        condition_query = ''
        params = None
    else:
        condition_query = " WHERE " + " AND ".join([f"{key} = ?" if not isinstance(value, list) else f"{key} IN ({','.join(['?'] * len(value))})" for key, value in conditions.items()])
        # Flatten the parameter values if any are lists (for the IN clause)
        params = tuple([item for value in conditions.values() for item in (value if isinstance(value, list) else [value])])
    
    query = f"SELECT * FROM {table_name} {condition_query}"

    df = pd.read_sql_query(query, connection, params=params)
    
    return df
