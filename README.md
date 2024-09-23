# Personal Python Packages

A personal collection of lightweight packages for my own personal projects. Mostly created for Python projects.

# Different packages
- **SQLite ORM**: Lightweight SQLite ORM and utilities for database handling.
  - Includes extras for functions with Pandas.
- **Data Analysis tools**: Classes and independent functions dedicated to data-cleaning, plotting, excel usage, etc...
- **UI tools**: At the moment, contains basic functions for basic addition of CLI functions.

A personal collection of reusable functions, classes, and utilities for data analysis, database handling, user interfaces, and more. This package is designed to make your Python projects easier to manage and scale by providing a variety of custom modules for different tasks.

# Installation and usage

This repository includes different packages, all of which can be installed from GitHub, either cloning the repository or installing locally.

## SQLite ORM:
For the basic module:
        
        pip install "own_sqlite_orm[sqlite] @ git+https://github.com/LoloCG/PersonalPythonPackage.git#subdirectory=Databases/own_sqlite_orm"
        
development branch:

        pip install "own_sqlite_orm[sqlite] @ git+https://github.com/LoloCG/PersonalPythonPackage.git@development#subdirectory=Databases/own_sqlite_orm"

If the Pandas module extras is required:

        pip install "own_sqlite_orm[sqlite_pandas] @ git+https://github.com/LoloCG/PersonalPythonPackage.git#subdirectory=Databases/own_sqlite_orm"


Inside the python file, the import can be made with:

        from own_sqlite_orm import *

## Example usage

        from own_sqlite_orm import ORMManager, DBConnector, TableManager, CRUDManager, convert_dict_valType_to_sqlType

        db = SQLiteDatabase('my_database.db')

        columns = {
        'col1': 'TEXT',
        'col2': 'INTEGER'}
        db.sql_dict_to_columns(columns)
        db = ORMManager(db_name='example.db', db_path=None)

        db.create_table(table_name='table_example.db')
