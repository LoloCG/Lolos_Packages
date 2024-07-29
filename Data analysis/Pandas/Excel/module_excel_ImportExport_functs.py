import os
import pandas as pd

# important functions:
    # to import module use, Add the directory containing your module to sys.path, then import the module:
        #import sys

        # sys.path.append(r'C:\Users\Lolo\Desktop\Programming\GITRepo\PythonLearn-Resources\Data analysis\Pandas\Excel')
        # module_excel_ImportExport_functs = __import__('module_excel_ImportExport_functs')

    # the two following used to obtain the path of the script, then to join them with the file selected.
        # main_dir = os.path.dirname(os.path.abspath(__file__))
        # file_path = os.path.join(main_dir, chosen_file)

    # used to directly open .csv files and load them into a dictionary DataFrame, as these do not have multiple sheets. 
        # df_dict = pd.read_csv(file_path)
        # Some cases may require to specify the encoding, delimiter and to skip rows
        # df_dict = pd.read_csv(file_path, encoding='utf-16', delimiter=';', skiprows=1)

    # To change from "," to "." in a column:
        # dataframe['column'] = dataframe['column'].str.replace(',', '.').astype(float)

def show_folder_excel_files(folder_dir, file_type = None):
    '''
    Searches the folder given for any excel extension file, printing any that exist and returning a list of the file names.
    
    Parameters:
    folder_dir (str): The directory to search for Excel files.

    
    folder_excels (list): a list of strings of the excel files that are located in the folder direction.
    '''
    if not os.path.exists(folder_dir):
        print(f"Directory {folder_dir} does not exist.")
        return []
    if not os.path.isdir(folder_dir):
        print(f"{folder_dir} is not a directory.")
        return []
    
    folder_files = os.listdir(folder_dir)
    folder_excels = [file for file in folder_files if file.endswith(('.csv', '.xlsx', '.xls', '.xlsm'))]

    print("Files in the folder:")
    for index, file in enumerate(folder_excels):
        print(f"{index + 1}: {file}")

    return folder_excels

def select_excelFile_fromFolder(folder_dir, file_type = None):
    input_excels = show_folder_excel_files(folder_dir,file_type)
    
    while True:
        try:
            choice = int(input(f"Enter the number of the file you want to open (1-{len(input_excels)}): "))
            if 1 <= choice <= len(input_excels):
                chosen_file = input_excels[choice - 1]
                break
            else:
                print(f"Please enter a number between 1 and {len(input_excels)}.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    print(f"chosen file: {chosen_file}")
    print()
    
    return chosen_file

def select_excelSheets_fromFile(file_path):

    # Determine the engine based on file extension
    if file_path.endswith('.xlsx') or file_path.endswith('.xlsm'):
        excel_file = pd.ExcelFile(file_path, engine='openpyxl')
    elif file_path.endswith('.xls'):
        excel_file = pd.ExcelFile(file_path, engine='xlrd')
    else:
        raise ValueError("Unsupported file format. \nPlease provide a .xlsm, .xlsx, or .xls file.")
        return

    sheet_names = excel_file.sheet_names
    
    for index, sheet in enumerate(sheet_names):
        print(f"{index + 1}: {sheet}")
    
    user_input = input("Select sheets to load \n(comma-separated, or blank for all): ")

    if user_input.strip() == "":
        selected_sheets = sheet_names
    else:
        selected_indices = [int(i) - 1 for i in user_input.split(',')]
        selected_sheets = [sheet_names[i] for i in selected_indices]
    
    print(f"selected sheets: {str(selected_sheets)}")
    print()

    return selected_sheets

def detect_CSV_header_row(file_path): # AT THE MOMENT ONLY DETECTS IF INDEX 1 or 0!!!
    '''
    Detects if the header row in a CSV file is at index 1 instead of index 0.
    
    This function reads the first two rows of the file with different encodings and delimiters,
    compares their lengths, and decides whether the first row is a title or a header.

    Parameters:
    file_path (str): The path to the CSV file.

    Returns:
    int: 1 if the headers are at index 1 (indicating to skip the first row), 0 if the headers are at index 0.
    '''
    encodings = ['utf-8', 'utf-8-sig', 'latin1', 'iso-8859-1', 'cp1252']
    delimiters = [',', ';', '\t']

    for encoding in encodings:
        for delimiter in delimiters:
            try:
                with open(file_path, 'r', encoding=encoding) as file:
                    first_row = len(file.readline().strip().split(delimiter))
                    second_row = len(file.readline().strip().split(delimiter))
                    ''' DEBUG CODE
                    print()
                    print(f"deli = {delimiter}, encoding = {encoding}")
                    print(f"length of first row {first_row}, second row {second_row}")
                    print("first row > 1 =", first_row > 1)
                    print("first row >= second row =",first_row >= second_row)
                    '''
                    if first_row > 1 and first_row >= second_row: 
                        # maybe?: come with a better criteria. In theory:
                            # first row should be > 1, 
                            # first row should be equal or greater than second
                        print("Headers found in index 0")
                        return 0  # Skip the first row                  
            except:
                continue

    print("Headers found in index 1")
    return 1

def detect_encoding(file_path): # NOT USED, REQUIRES CHARDET LIBRARY
    '''
    Detect encoding using chardet

    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read(10000))
    return result['encoding']
    '''

def CSV_file_to_df_bruteforce(file_path):
    """
    Used to import .cvs files to a DataFrame, if the encoding, delimiters and whether the first or second row is used as header.
    Used mostly as a test for importing .csv files for Abstract Spoon's ToDoList app.

    Calls the function detect_CSV_header_row to check if it is required to start on second row.
    Tries by brute force different encoding methods and delimiters until one fits the criteria of 
        not being empty, no unnamed columns, more than 1 column...
    
    Parameters:
    file_path (str): The path to the CSV file.

    Returns:
    df_raw (dataframe): the df with all information without any cleanup
    """
    encodings = ['utf-8', 'utf-8-sig', 'utf-16', 'latin1', 'iso-8859-1', 'cp1252']
    delimiters = [',', ';', '\\', '\t'] 

    skiprows = detect_CSV_header_row(file_path)
    print()

    for enc in encodings:
        for delim in delimiters:
            try:
                print(f"enc = {enc}, delim = {delim}")
                df_raw = pd.read_csv(file_path, encoding=enc, delimiter=delim, skiprows=skiprows)
            
                if df_raw.empty:
                    print("df empty error, continuing")
                    continueS
                elif any(df_raw.columns.str.startswith('Unnamed')):
                    print(f"columns start with unnamed error ({len(df_raw.columns.str.startswith('Unnamed'))})")
                    continue
                elif not len(df_raw.columns) > 1:
                    print(f"less than 2 columns error ({len(df_raw.columns)})")
                    print(df_raw.columns)
                    continue

                else:
                    return df_raw

            except pd.errors.ParserError:
                print(f"Parser error")
                continue
            except UnicodeDecodeError:
                print(f"Unicode decode error")
                continue

    return None
