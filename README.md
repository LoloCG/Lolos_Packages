# PersonalPythonPackage

A personal collection of reusable functions, classes, and utilities for data analysis, database handling, user interfaces, and more. This package is designed to make your Python projects easier to manage and scale by providing a variety of custom modules for different tasks.

## Features

- **Database Utilities**: Lightweight SQLite ORM and utilities for database handling.
- **Data Analysis**: Custom functions and extensions for working with pandas.
- **Plotting**: Functions for generating plots using `matplotlib`, `numpy`, and `pandas`.
- **User Interfaces**: UI utilities using `PySide6` or terminal-based UIs with `curses`.

---

## Installation

You can install this package directly from GitHub without needing to clone the repository, or you can clone it and install it locally. You also have the option to install specific modules or utilities based on your project needs.

### Installing the Package without Cloning the Repository

To install the entire package directly from GitHub:

        pip install git+https://github.com/LoloCG/PersonalPythonPackage.git

### Installing Specific Modules

If you only want to install specific modules (for example, the SQLite utilities):

        pip install git+https://github.com/LoloCG/PersonalPythonPackage.git#egg=PersonalPythonPackage[sqlite]

You can replace sqlite with other options such as `pandas`, `plotting`, or `pyside` based on what you need.


### Cloning and Installing the Repository Locally

If you prefer to clone the repository and install it locally:

        git clone https://github.com/LoloCG/PersonalPythonPackage.git

Navigate to the root directory (where setup.py is located) and install the package in editable mode:

    pip install -e .

### Installing with Optional Dependencies

You can install the package with optional dependencies based on the specific utilities you want to use.
Example, installing only the SQLite utilities:

        pip install PersonalPythonPackage[sqlite]

Installing all utilities:

        pip install PersonalPythonPackage[sqlite, pandas, plotting, pyside]

## Usage After Installation
Once the package is installed, you can import and use the available modules. 
SQLite Utilities Example:

        from personalpythonpackage.databases.sqlite_orm.basics import SQLiteDatabase

        db = SQLiteDatabase('example.db')

        db.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)')
