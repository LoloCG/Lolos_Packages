

### Installing the Package without Cloning the Repository

To install the entire package directly from GitHub:

        pip install git+https://github.com/LoloCG/PersonalPythonPackage.git

### Installing Specific Modules

If you only want to install specific modules (for example, the SQLite utilities):

        pip install 'PersonalPythonPackage[sqlite] @ git+https://github.com/LoloCG/PersonalPythonPackage.git'


You can replace sqlite with other options such as `pandas`, `plotting`, or `pyside` based on what you need.

        pip install 'PersonalPythonPackage[pandas] @ git+https://github.com/LoloCG/PersonalPythonPackage.git'


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
