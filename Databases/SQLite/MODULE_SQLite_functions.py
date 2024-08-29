import sqlite3
import os

r'''
sys.path.append(r'C:\Users\Lolo\Desktop\Programming\GITRepo\PythonLearn-Resources\Databases\SQLite')
import MODULE_SQLite_functions

TODO:
    - create "check_db_connection" internal method, wwhere it uses the folloing code + other error handling techniques...         
'''

class DatabaseHandler:
    def __init__(self, db_dir, db_name=None):
        """Initialize with the database name and directory.

        Args:
            db_name (str): The name of the database file.
            db_dir (str): The directory where the database file is stored.
        """
        if db_dir is None:
            raise ValueError("Database directory must be provided upon creation")

        self.db_name = db_name
    
        if self.db_name is None:
            self.db_name = 'Database.db'
            print(f"No database name was given. Using '{self.db_name}' as the name")
        elif not isinstance(db_name, str):
            raise ValueError(f"\ndb_name should be a string.\ndb_name type is {isinstance(self.db_name,str)}\n")    
        elif not self.db_name.endswith('.db'):
            self.db_name = self.db_name + ".db"

        self.db_path = os.path.join(db_dir, self.db_name)
        self.connector = None
        self.cursor = None
        self.database_name = None
        self.main_table_name = None
        self.db_table_names = []

    def create_db_table(self, table_items, table_name=None, verbose=None):
        '''
        table_items (dict), key = str, item = SQLdatatype
        mainTable_name (str)

        '''
        if not self.check_db_existance():
            print(f"Setting database {self.db_name} with direction {self.db_path}")

        self.connector = sqlite3.connect(self.db_path)
        self.cursor = self.connector.cursor()

        if table_name is None and self.main_table_name is None:
            self.main_table_name = 'main_table'
            table_name = self.main_table_name
        elif self.main_table_name is None:
            self.main_table_name = table_name
            print(f"Setting the main table name as {table_name}")

        print(f"Creating {self.db_name} database table with name '{table_name}'...")

        if verbose:
            print("Items in table:")
            for item, types in table_items.items():
                print(f"\t{item}")

        columns = ", ".join([f'"{col}" {dtype}' for col, dtype in table_items.items()])
        
        create_table_query = f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            {columns}
        )
        '''
        self.cursor.execute(create_table_query)
        self.connector.commit()

    def convert_dict_valType_to_sqlType(self, dtype_dict):
        #print("Converting values from dtype to SQL type values...")
        
        sql_dict = {}

        for key, item in dtype_dict.items():
            dtype = type(item)

            sql_type = None
            if dtype in [int, 'int64', 'int32']:            # Handling ints
                sql_type = 'INTEGER'
            elif dtype in [float, 'float64', 'float32']:    # Handling floats
                sql_type = 'REAL'  
            elif dtype == str or dtype == 'O':              # Handling strings and object types
                sql_type = 'TEXT'
            elif str(dtype).startswith('datetime64'):       # Handling datetime from Pandas
                sql_type = 'TEXT'  # alternatively, use DATETIME format if required...
                
            elif dtype == list:
                print(f"!!! - List datatype in dictionary ({key}). Will be stored as concatenated string.")
                sql_type = 'TEXT' 
            else:
                raise ValueError(f"Unrecognized dtype ({dtype}) key: {key}")
                pass
            #print(f"DEBUG: Key ({key}) set as {sql_type}")
            
            sql_dict[key] = sql_type
        
        return sql_dict
    
    def check_db_existance(self): 
        """Check if the SQLite database file already exists.

        Returns:
            bool: True if the database exists, False otherwise.
        """
        if os.path.exists(self.db_path):
            #print(f"db path is: {self.db_path}")
            return True 
        else:
            print(f"Database does not exist.")
            return False

    def table_has_items(self, table_name=None):
        if not table_name:
            table_name = self.main_table_name
        
        self.check_db_connection(connect=True)
        self.cursor.execute(f"SELECT COUNT(1) FROM {table_name};")
        return self.cursor.fetchone()[0] > 0

    def insert_data_from_df(self, dataframe,table_name=None):
        import pandas as pd
        if not isinstance(dataframe, pd.DataFrame):
            raise TypeError(f"The variable passed to insert data to database is not dataframe type. It is '{type(dataframe)}'")
        
        if not table_name:
            table_name = self.main_table_name

        try:
            dataframe.to_sql(table_name, self.connector, if_exists='append', index=False)
            self.connector.commit()
            print(f"Data inserted successfully into {table_name}")
            
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            self.connector.rollback()

    def close_connection(self):
        print(f"Closing connection to database.")
        if self.cursor:
            self.cursor.close()
            self.cursor = None
        if self.connector:
            self.connector.close()
            self.connector = None
   
    def check_db_connection(self, connect=False):
        if self.connector is None or self.cursor is None:
            if connect == True:
                # print(f"DEBUG: Connector or cursor is None, creating connection to db")
                self.connector = sqlite3.connect(self.db_path)
                self.cursor = self.connector.cursor()

    def retrieve_rows_as_dicts(self, search_parameters_dict, table_name=None):
        '''
            Retrieves data from the specified database table based on the parameters provided 
                in the search_parameters_dict. Each row of the result is returned as a dictionary 
                with column names as keys and corresponding row values as values.
            
            Parameters:
                search_parameters_dict: A dictionary where the key is the column name and 
                    the value is the value to search for in that column.
                table_name: (Optional) The name of the table to query. If not provided, 
                    defaults to the main_table_name.

            Returns: 
                A list of dictionaries, where each dictionary represents a row from 
                    the database. Returns None if an error occurs.
        '''

        if table_name is None:
            table_name = self.main_table_name

        try:
            print(f"Retrieving data from {table_name}...")
            
            sql_query = f"SELECT * FROM {table_name} WHERE "

            value_list = []
            n = 0
            for column, value in search_parameters_dict.items():
                value_list.append(value)
                sql_query += str(column) + ' = ?'
                n += 1
                if n < len(search_parameters_dict):
                    sql_query += ' AND '
            
            self.cursor.execute(sql_query, value_list)
            rows = self.cursor.fetchall()

            # Get column names from the cursor description 
            column_names = [description[0] for description in self.cursor.description]

            # Convert each row to a dictionary
            result_dicts = [dict(zip(column_names, row)) for row in rows]
            
            return result_dicts

        except sqlite3.Error as e:
            # Print the error message
            print(f"An error occurred: {e}")
            return None

    def get_last_table_value_of_columns(self, column_names, columns_to_order, table_name=None):
        if table_name is None:
            table_name = self.main_table_name
        
        query = f"""
            SELECT {column_names}
            FROM {table_name}
            ORDER BY {columns_to_order} DESC
            LIMIT 1;
            """
        
        if self.cursor is None:
            self.connector = sqlite3.connect(self.db_path)
            self.cursor = self.connector.cursor()

        self.cursor.execute(query)
        result = self.cursor.fetchone()
            
        # If only one column is selected, return the value directly
        if len(column_names.split(',')) == 1:
            return result[0] if result else None
        else:
            return result if result else None

    def retrieve_all_data_as_df(self, tableName=None):
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

    def check_table_existance(self, table_name, verbose=False):
        
        '''
        if self.connector == None: 
            print(f"While checking for connector in table existance, it shows None")
            
        '''
        self.cursor.execute(f"PRAGMA table_info({table_name});")

        # Fetch the results
        result = self.cursor.fetchall()

        # Check if the table exists
        if result:
            if verbose: print(f"Table '{table_name}' exists.")
            return True
        else:
            if verbose: print(f"Table '{table_name}' does not exist.")
            return False

    def insert_data_from_dict(self, data_dict, table_name,verbose=False):
        
        if not table_name:
            table_name = self.main_table_name

        # Construct the SQL query components
        keys = ", ".join(data_dict.keys())
        question_marks = ", ".join(["?" for _ in data_dict])
        values = tuple(data_dict.values())

        insert_query = f"INSERT INTO {table_name} ({keys}) VALUES ({question_marks})"
        
        # Execute the query with error handling
        try:
            self.cursor.execute(insert_query, values)
            self.connector.commit()
            if verbose: 
                print(f"Data inserted successfully into {table_name}")
                print(f"\tinserted: {len(values)} values")
            
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            self.connector.rollback()


# ==================== NOT USED ====================
def check_db_isupdated(self, newData): #TODO: not implemented nor tested at the moment

    self.connector = sqlite3.connect(self.database_name)
    self.cursor = self.connector.cursor()

    existing_columns = [description[0] for description in self.cursor.execute("PRAGMA table_info(tasks)").fetchall()]
    new_columns = list(newData.keys())
    
    return set(existing_columns) == set(new_columns)

def update_db(self, newData): #TODO: not implemented nor tested at the moment

    if not self.check_db_isupdated(newData):
        # Add any new columns
        for col, dtype in newData.items():
            self.cursor.execute(f"ALTER TABLE tasks ADD COLUMN {col} {dtype}")

    # To update rows, you'll need to have a method of identifying the rows to update,
    # such as an ID or another unique identifier. Example given is for adding/updating a row.
    keys = ", ".join(newData.keys())
    question_marks = ", ".join(["?" for _ in newData])
    values = tuple(newData.values())
    insert_query = f"INSERT INTO tasks ({keys}) VALUES ({question_marks})"
    self.cursor.execute(insert_query, values)
    self.connector.commit()



def update_db(self, update_data, identifier):
    """Updates a row in the tasks table based on a unique identifier."""
    set_clause = ", ".join([f"{key} = ?" for key in update_data.keys()])
    update_values = list(update_data.values())
    update_values.append(identifier)
    update_query = f"UPDATE tasks SET {set_clause} WHERE id = ?"
    self.cursor.execute(update_query, tuple(update_values))
    self.connector.commit()
