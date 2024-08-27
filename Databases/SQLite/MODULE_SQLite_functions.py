import sqlite3
import os

r'''
sys.path.append(r'C:\Users\Lolo\Desktop\Programming\GITRepo\PythonLearn-Resources\Databases\SQLite')
import MODULE_SQLite_functions

TODO:
    - create "check_db_connection" internal method, where it uses the following code + other error handling techniques...         
        if self.connector is None or self.cursor is None:
            print(f"DEBUG: connector or cursor is None, creating connection to db")
            self.connector = sqlite3.connect(self.db_path)
            self.cursor = self.connector.cursor()
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

    def create_db_table(self, tableItems, mainTable_name=None):
        '''
        tableItems (dict), key = str, item = SQLdatatype
        mainTable_name (str)

        '''
        print(f"Setting database {self.db_name} with direction {self.db_path}")
        self.connector = sqlite3.connect(self.db_path)

        self.cursor = self.connector.cursor()
    
        if mainTable_name is None:
            self.main_table_name = 'main_table'
        else:
            self.main_table_name = mainTable_name

        print(f"Creating {self.db_name} database table with name '{self.main_table_name}'...")

        columns = ", ".join([f'"{col}" {dtype}' for col, dtype in tableItems.items()])

        create_table_query = f'''
        CREATE TABLE IF NOT EXISTS {self.main_table_name} (
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
            print(f"db path is: {self.db_path}")
            return True 
        else:
            return False

    def insert_data_from_df(self, dataframe):
        import pandas as pd
        if not isinstance(dataframe, pd.DataFrame):
            raise TypeError(f"The variable passed to insert data to database is not dataframe type. It is '{type(dataframe)}'")

        dataframe.to_sql(self.main_table_name, self.connector, if_exists='append', index=False)
        self.connector.commit()

    def close_connection(self):
        if self.cursor:
            self.cursor.close()
            self.cursor = None
        if self.connector:
            self.connector.close()
            self.connector = None
            
    def retrieve_data_as_df(self, tableName=None):
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

class Unused:
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

    def insert_data(self, data):
        """Inserts data into the tasks table."""
        keys = ", ".join(data.keys())
        question_marks = ", ".join(["?" for _ in data])

        values = tuple(data.values())

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
    