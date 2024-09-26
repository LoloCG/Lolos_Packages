import sqlite3

class DBManager:
    def __init__(self, db_name=None, db_path=None, auto_commit=True):
        self.db_name = db_name
        if self.db_name is None:
            self.db_name = 'Database.db'
        elif not self.db_name.endswith('.db'):
            self.db_name = self.db_name + ".db"

        # print(f"Database Name set as {self.db_name}")

        self.db_path = db_path or './'
        self.auto_commit = auto_commit

        self.connector = Connector(self.db_path, self.db_name, self.auto_commit)

        self.table_manager = TableManager(self.connector)
        self.crud_manager = CRUDManager(self.connector)

    def get_connector(self):
        return self.connector

class Connector:
    def __init__(self, db_path, db_name, auto_commit):
        self.db_path = db_path
        self.db_name = db_name
        self.auto_commit = auto_commit

        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.auto_commit:
            self.commit()
        self.close()

    def connect(self):
        full_path = f"{self.db_path}/{self.db_name}"
        self.conn = sqlite3.connect(full_path)

        return self.conn

    def commit(self):
        if self.conn:
            self.conn.commit()

    def close(self):
        if self.conn:
            self.conn.close()

    def execute(self, query, params=None):
        cursor = self.conn.cursor() 
        cursor.execute(query) if not params else cursor.execute(query, params)
        if self.auto_commit:
            self.commit()
        return cursor
        
class TableManager:
    def __init__(self, connector):
        self.connector = connector

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
        
        self.connector.execute(final_table_query)

        return self
    
    def sql_dict_to_columns(self, items_dict):
        '''        
            items_dict (dict): key = str (column name), item = SQL datatype
        '''
        self.table_columns = ", ".join([f'"{col}" {dtype}' for col, dtype in items_dict.items()])
        return self
    
    def add_primary_key(self, primary_key):
        '''
            primary_key (str): Column name to be set as the primary key (optional).
        '''
        if primary_key == None: self.primary_key_clause = None
        else: self.primary_key_clause = f', PRIMARY KEY ("{primary_key}")'
        return self

    def add_foreign_keys(self, foreign_keys):
        '''
            foreign_keys (dict): dictionary where each key = str (foreign key column), 
                value = ('referenced_table', 'referenced_column').
        ''' 
        self.connector.execute("PRAGMA foreign_keys = ON")

        self.foreign_key_clauses = ", " + ", ".join([
                f'FOREIGN KEY ("{fk_column}") REFERENCES {referenced_table}({referenced_column})'
                for fk_column, (referenced_table, referenced_column) in foreign_keys.items()
            ])
        return self

    def table_exists(self, table_name):
        """Check if a specific table exists in the database"""
        
        cursor = self.connector.conn.cursor()
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        table = cursor.fetchone()
        return table is not None

    def table_rows(self, table_name):
        """Check the rows of a table"""
        try:
            cursor = self.connector.conn.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            row_count = cursor.fetchone()[0]
            return row_count
            
        except sqlite3.OperationalError as e:
            # Check if the error message mentions the table doesn't exist
            if 'no such table' in str(e):
                print(f"Error: The table '{table_name}' does not exist.")
            else:
                print(f"OperationalError: {e}")
            return None
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
            return None

    def check_table(self, table_name):
        """Check if a table exists and has rows"""
        exists = self.table_exists(table_name)
        if exists:
            has_rows = self.table_rows(table_name)
            return exists, has_rows
        else:
            return exists, False

    def list_tables(self): # REFACTOR
        """List all tables in the database"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [table[0] for table in cursor.fetchall()]
        return tables

class CRUDManager:
    def __init__(self, connector):
        self.connector = connector

    def direct_execute(self, query, params=None):
        """Execute an SQL query and return the cursor"""
        
        self.connector.execute(query, values)

    def insert_from_dict(self, data_dict, table_name):
        if not data_dict:
            raise ValueError("Cannot insert empty dictionary into database table.")

        keys = ", ".join(data_dict.keys())
        question_marks = ", ".join(["?" for _ in data_dict])
        values = tuple(data_dict.values())

        insert_query = f"INSERT INTO {table_name} ({keys}) VALUES ({question_marks})"
            
        self.connector.execute(insert_query, values)

def dict_to_sqlType(dtype_dict):
    from datetime import date
    
    sql_dict = {}
    for key, item in dtype_dict.items():

        sql_type = None
        if isinstance(item, int): # pd.api.types.is_integer_dtype(item) or 
            sql_type = 'INTEGER'
        elif isinstance(item, float): # pd.api.types.is_float_dtype(item) or 
            sql_type = 'REAL'
        elif isinstance(item, str): # pd.api.types.is_string_dtype(item) or 
            sql_type = 'TEXT'
        elif isinstance(item, date): # or pd.api.types.is_datetime64_any_dtype(item)
            sql_type = 'TEXT'       # Store datetime.date as TEXT in 'YYYY-MM-DD' format
        elif item == list:
            print(f"!!! - List datatype in dictionary ({key}). Will be stored as concatenated string.")
            sql_type = 'TEXT'
        else:
            raise ValueError(f"Unrecognized dtype ({type(item)}) key: {key}")
            pass
        
        sql_dict[key] = sql_type
    
    return sql_dict