# Installation
## Installing the Package without cloning the repository

        pip install git+https://github.com/LoloCG/PersonalPythonPackage.git

or to download specific modules from the package:

        pip install git+https://github.com/LoloCG/PersonalPythonPackage.git#egg=PersonalPythonPackage[sqlite]

## Cloning and installing the repository locally

        git clone https://github.com/LoloCG/PersonalPythonPackage.git

From the root folder of the package (where setup.py is located), run the installation command.
For installing all modules in the package:

        pip install -e .

### To install package with optional dependencies:

- example: Install only the SQLite utilities:

        pip install PersonalPythonPackage[sqlite]

- Install all utilities:
    
        pip install PersonalPythonPackage[sqlite, basic_data_analysis, plotting_data_analysis, pyside, curses]

# Usage After Installation
- SQLite utils:
  
        from personalpythonpackage.databases.sqlite_utils import DatabaseHandler

- pandas_basic_utils:

        from personalpythonpackage.data_analysis.pandas_basic_utils import *

