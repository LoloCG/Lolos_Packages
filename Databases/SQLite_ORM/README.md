# Installation

    pip install "SQLite_ORM[sqlite] @ git+https://github.com/LoloCG/Lolos-Packages.git#subdirectory=Databases/SQLite_ORM"

## Extras with dependencies

- `SQLite_ORM[pandas_addon]`

        pip install "SQLite_ORM[pandas_addon] @ git+https://github.com/LoloCG/Lolos-Packages.git#subdirectory=Databases/SQLite_ORM"

# Example usage:
Basic python code:

    from SQLite_ORM.basics import *

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

## Example usage with Pandas:

    # Generate the manager object
    db = DBManager(db_name=db_name, db_path=db_path)

    # From it obtain connector object, and connect to database.
    db.connector.connect()
    connector_obj = db.get_connector()

    # Use the connector for the dataframe function, and close connection.
    insert_data_from_df(dataframe=df, connector_obj=connector_obj, table_name=main_table_name)
    db.connector.close()