import os
import pandas as pd
r'''
sys.path.append(r'C:\Users\Lolo\Desktop\Programming\GITRepo\PythonLearn-Resources\Data analysis\Pandas\Excel')
from MODULE_pandas_excel_functions import ExcelDataExtract
'''
# ========================= MODULE_pandas_excel_functions/ExcelDataExtract =========================
# =================================== 2024/02/09 =========================
class ExcelDataExtract:
    def __init__(self, file_folder_dir = None, chosen_file = None):
        self.main_dir = os.path.dirname(os.path.abspath(__file__))
        self.file_folder_dir = file_folder_dir
        self.chosen_file = None
        self.file_type = None

        self.excels_in_folders = []

        self.selected_sheets = None

        self.dataframe = None
        self.dataframe_type = None

    def load_excel_to_dataframe_dict(self, selected_sheets=None, importNaN=True):
        df_dict = {}
        full_file_path = os.path.join(self.file_folder_dir, self.chosen_file)

        sheets_to_load = selected_sheets if selected_sheets else self.selected_sheets

        for sheet in self.selected_sheets:
            print(f"loading {sheet} into dataframe dictionary")

            df = pd.read_excel(full_file_path, sheet_name=sheet)
            
            if importNaN: # First drops columns that have NaN or empty string as headers, then columns where all values are NaN
                df = df.loc[:, df.columns.notnull()]
                df = df.loc[:, df.columns != '']
                df = df.dropna(axis=1, how='all')
                
            df_dict[sheet] = df

        self.dataframe = df_dict
        self.dataframe_type = type(self.dataframe) # Ensures that the dataframe type is <class 'dict'>
        
        #DEBUG: print(f"debug. df type: {self.dataframe_type}\n")

    def load_csv_to_dataframe(self, chosen_file, encoding=None, delimiter=None, skiprows=None):
        self.chosen_file = chosen_file

        targetfile_path = os.path.join(self.file_folder_dir, self.chosen_file)
        print(f"Extracting file {chosen_file} from path {targetfile_path}")
        
        df_raw = pd.read_csv(targetfile_path, encoding='utf-16', delimiter='\t', skiprows=1) # TODO: make dynamic selector of encoding, delimiter, skiprows...
        
        #DEBUG: print(f"Extracted df:\n{df_raw.head()}") 
        #DEBUG: print(f"returning type: {type(df_raw)}")

        self.dataframe = df_raw

    def get_folder_excel_files(self, file_folder_dir=None, file_type = None):
        '''
        Searches the folder given for any excel extension file, printing any that exist and returning a list of the file names.
        
        Parameters:
        file_folder_dir (str): The directory to search for Excel files.

        Returns:
        folder_excels (list): a list of strings of the excel files that are located in the folder direction.
        '''
        self.file_folder_dir = file_folder_dir

        if not os.path.exists(file_folder_dir):
            print(f"Directory {file_folder_dir} does not exist.\n")
            return []
        if not os.path.isdir(file_folder_dir):
            print(f"{file_folder_dir} is not a directory.\n")
            return []
        
        folder_files = os.listdir(file_folder_dir)
        self.excels_in_folders = [file for file in folder_files if file.endswith(('.csv', '.xlsx', '.xls', '.xlsm'))]

        print("Files in the folder:")
        for index, file in enumerate(self.excels_in_folders):
            print(f"{index + 1}: {file}")

    def select_excelFile_fromFolder(self, excels_in_folders=None):
        while True:
            try:
                choice = int(input(f"Enter the number of the file you want to open (1-{len(self.excels_in_folders)}): "))
                if 1 <= choice <= len(self.excels_in_folders):
                    file = self.excels_in_folders[choice - 1]
                    break
                else:
                    print(f"Please enter a number between 1 and {len(self.excels_in_folders)}.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

        print(f"chosen file: {file}")
        
        self.chosen_file = file
    
    def select_excelSheets_fromFile(self, full_file_path=None):
        '''
        '''
        full_file_path = os.path.join(self.file_folder_dir, self.chosen_file)

        # Determines the engine based on file extension
        if full_file_path.endswith('.xlsx') or full_file_path.endswith('.xlsm'):
            excel_file = pd.ExcelFile(full_file_path, engine='openpyxl')
        elif full_file_path.endswith('.xls'):
            excel_file = pd.ExcelFile(full_file_path, engine='xlrd')
        else:
            raise ValueError("Unsupported file format. \nPlease provide a .xlsm, .xlsx, or .xls file.")
            return

        sheet_names = excel_file.sheet_names
        
        for index, sheet in enumerate(sheet_names):
            print(f"{index + 1}: {sheet}")
        
        user_input = input("Select sheets to load (comma-separated numbers, or enter blank for all): ")

        if user_input.strip() == "":
            self.selected_sheets = sheet_names
        else:
            selected_indices = [int(i) - 1 for i in user_input.split(',')]
            self.selected_sheets = [sheet_names[i] for i in selected_indices]
        
        print(f"selected sheets: {str(self.selected_sheets)}")
        print()

    def detect_csv_delimiter(self): # TODO: finish this function
        delimiters = [',', ';', '\\', '\t'] 
        
    def detect_csv_encoding(): # TODO: finish this function
        encodings = ['utf-8', 'utf-8-sig', 'utf-16', 'latin1', 'iso-8859-1', 'cp1252']

    def detect_csv_header_row():
        print("TODO...")

class ExcelGrapher:
    def __init__(self, dataframe: pd.DataFrame):
        self.dataframe = dataframe

    def add_excel_scatter_chart(self, output_excel_path): # TODO: Re-Do this whole function to make dynamic
        ''' 
        Creates a line-scatter chart in excel using a DataFrame Dictionary.
        
        Parameters
        output_excel_path (str): The file path for the output Excel file, including the .xlsx extension.
        df_dict (dict): A dictionary where each key is a series name and each value is a DataFrame containing 
                        numerical series data. Each DataFrame should have the same column names for X and Y values.
        '''
        
        with pd.ExcelWriter(output_excel_path, engine="xlsxwriter") as writer:
            workbook = writer.book

            for series_name, df in df_dict.items():
                print(f"Adding data from sheet: {series_name}")
                sheet_name = f"{series_name}" # Change to obtain new name
                df.to_excel(writer, sheet_name=sheet_name, index=False)
            
            # Create an empty df that will be used to create the chart
            empty_df = pd.DataFrame() 
            empty_df.to_excel(writer, sheet_name="Chart", index=False)
            worksheet = writer.sheets['Chart']
            chart = workbook.add_chart({'type': 'scatter'})

            first_df = next(iter(df_dict.values())) # Assumes all DataFrames have the same structure
            X_column = first_df.columns[0]  # Get the name of the first column
            Y_column = first_df.columns[1]  # Get the name of the second column
            chart_name = f"{X_column} vs {Y_column}"

            for sheet_name, df in df_dict.items():
                print(f"Plotting data from {sheet_name}")
                
                last_row = len(df)

                line_style = {'width': 2}
                chart.add_series({
                    'name':         f'{sheet_name}',
                    'categories':   [f"{sheet_name}", 1, 0, last_row, 0],
                    'values':       [f"{sheet_name}", 1, 1, last_row, 1],
                    'marker':       {'type': 'none'},
                    'line':         line_style,
                    'smooth':       True
                })

            chart.set_x_axis({
                'name': X_column, 
                'num_format': '0.00',  # Set number format to display 2 decimal places
                'position_axis': 'on_tick', # Positions the axis on the tick marks.
                'major_gridlines': {'visible': True},
                #'min': 0,
                #'max': last_value_mm,
                #'interval_unit': 50,
                #'interval_tick': 100 
                })
                    
            chart.set_y_axis({
                'name': Y_column,
                'num_format': '0.0',
                'major_gridlines': {'visible': True},
                })
            
            chart.set_legend({'position': 'bottom'})
            chart.set_title({'name': chart_name})
            chart.set_style(37)

            worksheet.insert_chart(0, 0, chart)
