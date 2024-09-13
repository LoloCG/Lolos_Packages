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

- Install only the SQLite utilities:

        pip install PersonalPythonPackage[sqlite]

- Install basic data analysis utilities:

        pip install PersonalPythonPackage[basic_data_analysis]

- Install the plotting utilities:

        pip install PersonalPythonPackage[plotting_data_analysis]

- Install PySide for UI:
        
        pip install PersonalPythonPackage[pyside]

- Install Curses for terminal UI:

        pip install PersonalPythonPackage[curses]

- Install all utilities:
    
        pip install PersonalPythonPackage[sqlite, basic_data_analysis, plotting_data_analysis, pyside, curses]


