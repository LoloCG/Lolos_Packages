def insert_data_from_df(dataframe, connector_obj, table_name):
    import pandas as pd
    import sqlite3

    if not isinstance(dataframe, pd.DataFrame):
        raise TypeError(f"The variable passed to insert data to database is not dataframe type. It is '{type(dataframe)}'")

    connection = connector.conn

    try:
        dataframe.to_sql(table_name, connection, if_exists='append', index=False)
        connection.commit()
        
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        connection.rollback()

def retrieve_all_data_as_df(self, tableName=None): # STILL NOT DONE
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
    