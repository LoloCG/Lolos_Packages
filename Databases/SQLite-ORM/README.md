# Installation

    pip install "SQLite-ORM[sqlite] @ git+https://github.com/LoloCG/Lolos-Packages.git#subdirectory=Databases/SQLite-ORM"
Development branch:

    pip install "SQLite-ORM[sqlite] @ git+https://github.com/LoloCG/Lolos-Packages.git@development#subdirectory=Databases/SQLite-ORM"

## Extras with dependencies

- `SQLite-ORM[sqlite_pandas]`

        pip install "SQLite-ORM[sqlite_pandas] @ git+https://github.com/LoloCG/Lolos-Packages.git#subdirectory=Databases/SQLite-ORM"

# Example usage:
Basic python code:

    from SQLite-ORM.basics import *

    # Initiate database manager instance
    db = DBManager(db_name='example.db', db_path=db_path) 

    db.connector.connect()
    
    # with table_manager, declare columns and create table.
    columns = {
        'col1': 'TEXT',
        'col2': 'INTEGER'}
    db.table_manager.sql_dict_to_columns(columns)
    table_name='table_example'
    db.table_manager.create_table(table_name)

    data_dict = {
        'col1': 'testItem',
        'col2': 3}    
    db.crud_manager.insert_from_dict(data_dict, table_name)

    db.connector.close()

Context manager can be used with the connector:

    db = DBManager(db_name='example.db', db_path=db_path)

    with db.connector: 
        # Rest of the code