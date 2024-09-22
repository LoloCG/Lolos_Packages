import sqlite3

'''
Basic CRUD Operations:
    insert_data_from_dict
    retrieve_rows_as_dicts
    update_rows
    delete_rows
    retrieve_all_data_as_df (if you use Pandas frequently)
'''
class ORMManager:
    def __init__(self, db_name=None, db_path=None, auto_commit=True):
        self.db_name = db_name
        if self.db_name is None:
            self.db_name = 'Database.db'
        elif not self.db_name.endswith('.db'):
            self.db_name = self.db_name + ".db"
        # print(f"Database Name set as {self.db_name}")

        self.db_path = db_path or './'
        self.auto_commit = auto_commit
        # self.auto_execute = auto_execute

        self.connector = DBConnector(self.db_path, self.db_name)
        self.table_manager = TableManager(self)
        self.crud_manager = CRUDManager(self)

    def commit(self):
        """Manual commit if auto_commit is False"""
        self.connector.commit()
        return self
    
    def _execute(self, query, params=None):
        """Executes a query and commits based on the auto_commit flag"""
        cursor = self.connector.execute(query, params)
        if self.auto_commit:
            self.commit()  
        return cursor

    def backup_database(self, backup_path):
        """Backup the current database to the specified backup path"""
        import shutil
        shutil.copyfile(f"{self.db_path}/{self.db_name}", backup_path)

class DBConnector:
    def __init__(self, db_path, db_name):
        self.db_path = db_path
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def connect(self):
        full_path = f"{self.db_path}/{self.db_name}"
        self.conn = sqlite3.connect(full_path)
        return self.conn

    def commit(self):
        """Commit changes to the database"""
        if self.conn:
            self.conn.commit()

    def close(self):
        if self.conn:
            self.conn.close()

    def check_integrity(self):
        """Check the integrity of the entire database"""
        cursor = self.conn.cursor()
        cursor.execute("PRAGMA integrity_check")
        return cursor.fetchone()[0] == "ok"
        
class TableManager:
    def __init__(self, connector):
        self.connector = connector

        self.cursor = self.connector.cursor()
        self.table_columns = None
        self.foreign_key_clauses = None
        self.primary_key_clause = None

    def create_table(self, table_name, autoincrement_id=True, table_cols=None):
        '''
            autoincrement_id (bool): Whether to automatically add an 'id' column with autoincrement.
        '''
        auto_id = 'id INTEGER PRIMARY KEY AUTOINCREMENT,' if autoincrement_id else ''

        if self.table_columns:
            columns = self.table_columns
        elif not table_cols:
            raise Exception(f"Table columns not declared during creation of {table_name}")

        if not self.foreign_key_clauses:
            foreign_key_clauses = ""
        else:
            foreign_key_clauses = self.foreign_key_clauses
        
        primary_key_clause = '' if not self.primary_key_clause else self.primary_key_clause

        final_table_query = f'''
            CREATE TABLE IF NOT EXISTS {table_name} (
                {auto_id}
                {columns}
                {foreign_key_clauses}
                {primary_key_clause}
            )'''
        # self.connector.execute(final_table_query)
        
        self.orm_manager._execute(final_table_query)

        return self
    
    def sql_dict_to_columns(self, items_dict):
        '''        
            items_dict (dict): key = str (column name), item = SQL datatype
        '''
        self.table_columns = ", ".join([f'"{col}" {dtype}' for col, dtype in items_dict.items()])
        return self
    
    def add_primary_keys(self, primary_key):
        '''
            primary_key (str): Column name to be set as the primary key (optional).
        '''
        self.primary_key_clause = f', PRIMARY KEY ("{primary_key}")'
        return self

    def add_foreign_keys(self, foreign_keys):
        '''
            foreign_keys (dict): dictionary where each key=foreign key column, and 
                    value=tuple containing the referenced table and column.
                    key = str (foreign key column), value = ('referenced_table', 'referenced_column')
        ''' 
        self.connector.conn.cursor().execute("PRAGMA foreign_keys = ON")

        foreign_key_clauses = ", " + ", ".join([
                f'FOREIGN KEY ("{fk_column}") REFERENCES {referenced_table}({referenced_column})'
                for fk_column, (referenced_table, referenced_column) in foreign_keys.items()
            ])
        return self

    def table_exists(self, table_name):
        """Check if a specific table exists in the database"""
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        table = cursor.fetchone()
        return table is not None

    def table_has_rows(self, table_name):
        """Check if a table has any rows"""
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        row_count = cursor.fetchone()[0]
        return row_count > 0

    def check_table(self, table_name):
        """Check if a table exists and has rows"""
        exists = self.table_exists(table_name)
        if exists:
            has_rows = self.table_has_rows(table_name)
            return exists, has_rows
        else:
            return exists, False

    def list_tables(self):
        """List all tables in the database"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [table[0] for table in cursor.fetchall()]
        return tables

class CRUDManager:
    def __init__(self, orm_manager):
        self.orm_manager = orm_manager
        self.connector = self.orm_manager.connector

    def direct_execute(self, query, params=None):
        """Execute an SQL query and return the cursor"""
        cursor = self.connector.conn.cursor() 
        cursor.execute(query, params or [])
        if self.orm_manager.auto_commit:
            self.orm_manager.commit()  # Commit automatically if auto_commit is True
        return cursor

def convert_dict_valType_to_sqlType(self, dtype_dict, verbose=False):
    import numpy as np
    import pandas as pd
    from datetime import date

    if verbose: print("Converting values from dtype to SQL type values...")
    
    sql_dict = {}
    for key, item in dtype_dict.items():

        sql_type = None
        if pd.api.types.is_integer_dtype(item) or isinstance(item, int):
            sql_type = 'INTEGER'
        elif pd.api.types.is_float_dtype(item) or isinstance(item, float):
            sql_type = 'REAL'
        elif pd.api.types.is_string_dtype(item) or isinstance(item, str):
            sql_type = 'TEXT'
        elif isinstance(item, date) or pd.api.types.is_datetime64_any_dtype(item):
            sql_type = 'TEXT'       # Store datetime.date as TEXT in 'YYYY-MM-DD' format
        elif item == list:
            print(f"!!! - List datatype in dictionary ({key}). Will be stored as concatenated string.")
            sql_type = 'TEXT'
        else:
            raise ValueError(f"Unrecognized dtype ({type(item)}) key: {key}")
            pass
        
        sql_dict[key] = sql_type
    
    return sql_dict




class DatabaseHandler: # This is the old code
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

    def create_db_table(self, table_items, table_name=None, 
        verbose=False, foreign_keys=None, 
        autoincrement_id=True, primary_key=None):
        '''
            table_items (dict): key = str (column name), item = SQL datatype
            table_name (str): Name of the table
            verbose (bool): Whether to print details during table creation
            autoincrement_id (bool): Whether to automatically add an 'id' column with autoincrement.
            primary_key (str): Column name to be set as the primary key (optional).
        '''
        if not self.check_db_existance():
            print(f"Setting database {self.db_name} with direction {self.db_path}")

        self.connector = sqlite3.connect(self.db_path)
        self.cursor = self.connector.cursor()
        
        if foreign_keys: self.cursor.execute("PRAGMA foreign_keys = ON")

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




        final_table_query = f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            {auto_id}
            {columns}
            {foreign_key_clauses}
            {primary_key_clause}
        )'''
        
        if verbose: print(f"Create Table Query: {create_table_query}")
        
        self.cursor.execute(create_table_query)
        self.connector.commit()

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

    def insert_data_from_df(self, dataframe,table_name=None, verbose=False):
        import pandas as pd
        if not isinstance(dataframe, pd.DataFrame):
            raise TypeError(f"The variable passed to insert data to database is not dataframe type. It is '{type(dataframe)}'")
        
        if not table_name:
            table_name = self.main_table_name

        try:
            dataframe.to_sql(table_name, self.connector, if_exists='append', index=False)
            self.connector.commit()
            if verbose: print(f"Data inserted successfully into {table_name}")
            
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

    def get_last_table_value_of_columns(self, column_names, columns_to_order, 
        table_name=None, limit='DESC', conditional=''):
        '''
            Retrieves the last value from a column in a table, with optional filtering.
            
            example usage:
                column_names='microcycle_num', 
                columns_to_order='microcycle_num', 
                table_name='table_name',
                conditional='weight_used IS NOT NULL'
        '''
        if table_name is None:
            table_name = self.main_table_name
        
        where_clause = f"WHERE {conditional}" if conditional else ""

        query = f"""
            SELECT {column_names}
            FROM {table_name}
            {where_clause}
            ORDER BY {columns_to_order} {limit}
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
                print(f"\tinserted: {len(values)} values ({values})")
            
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            self.connector.rollback()

    def bulk_update_rows(self, update_list_dicts, update_cols_list, table_name=None, verbose=False):
        '''
            Updates columns of multiple rows in the database using a batch operation.

            Parameters:
                - update_list_dicts: A list of dictionaries, where each dictionary contains the data for the update in the format
                    of key = column name, value = value to search for or to update.
                - update_cols_list (str): A list of columns to be updated in each row.
                - table_name: Optional. The table to update (defaults to self.main_table_name if not provided).
                - verbose: Optional. Prints detailed logs if True.

            Ensures all updates are executed within a single transaction, rolling back on error.
    
            # Example data for 2 exercises:
                update_cols_list = ['reps_list','sets_performed']
                update_list_dicts = [ 
                    {'reps_list':           '10,9,8',
                    'sets_performed':       3,
                    'microcycle_num':       1,
                    'session_num':          1,
                    'exercise_name':        'High bar squats'},
                    'reps_list':            '10,10,8,7',
                    'sets_performed':       4,
                    'microcycle_num':       1,
                    'session_num':          1,
                    'exercise_name':        'Bench press'}]
        '''
        if not table_name:
            table_name = self.main_table_name
        
        self.check_db_connection(connect=True)

        try:
            self.cursor.execute("BEGIN TRANSACTION;")

            if verbose: print(f"Queries of 'bulk_update_rows' method:")
            for update_dict in update_list_dicts:
                set_clause = None
                where_clause = None
                set_values = []
                where_values = []

                
                for dict_key, dict_val in update_dict.items():
                    # Construct the SET clause
                    if dict_key in update_cols_list:
                        if set_clause is None: 
                            set_clause = f"{dict_key} = ?"
                        else:
                            set_clause = f"{set_clause}, {dict_key} = ?"
                        set_values.append(dict_val)

                    # Construct the WHERE clause
                    else:
                        if where_clause is None:
                            where_clause = f" {dict_key} = ?"
                        else:
                            where_clause = f"{where_clause} AND {dict_key} = ?"
                        where_values.append(dict_val)

                query = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"
                if verbose: print(f"\tSET: {set_values}, WHERE: {where_values}")
                
                self.cursor.execute(query, tuple(set_values + where_values))

            self.connector.commit()
            if verbose: print("Bulk update of database successful.")

        except sqlite3.Error as e:
            self.connector.rollback()
            print(f"An error occurred: {e}")

        finally:
            self.close_connection()

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
