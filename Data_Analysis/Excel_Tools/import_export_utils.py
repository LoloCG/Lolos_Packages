import pandas as pd
import os

class ExcelImporter:
    def __init__(self):
        self.extraction_folder_dir = None
        self.file_to_extract = None
        self.sheets_to_extract = []

        # these are static at the moment...
        self.delimiter = None 
        self.encoding = None 
        self.skiprows = None

    def add_extraction_folder(self, folder_dir): # test further...
        if not os.path.exists(folder_dir):
            raise FileNotFoundError(f"Directory {folder_dir} does not exist.") # change to differen exception type
        elif not os.path.isdir(folder_dir):
            raise NotADirectoryError(f"{folder_dir} is not a directory.")
        else:
            self.extraction_folder_dir = folder_dir

        return self

    def add_file(self, file_name):
        self.file_to_extract = file_name
        
        if self.extraction_folder_dir:
            full_file_path = os.path.join(self.extraction_folder_dir, self.file_to_extract)
            if not os.path.exists(full_file_path):
                raise FileNotFoundError(f"The file '{self.file_to_extract}' does not exist in the directory '{self.extraction_folder_dir}'.")
            elif not os.path.isfile(full_file_path):
                raise IsADirectoryError(f"The path '{full_file_path}' is not a file.")

        # may require further validation in case of the file not containing termination

        return self

    def add_sheets(self, excel_sheets): # TODO
        # add validation to check if the provided sheets actually exist in the Excel file. 
        for sheet in excel_sheets:
            self.sheets_to_extract.append(sheet)
        
        return self

    def get_folder_excels(self, file_type:str=None):
        if not file_type:
            file_extension = ['.csv', '.xlsx', '.xls', '.xlsm']
        else:
            file_extension = file_type

        self.excels_in_folder = [file for file in os.listdir(self.extraction_folder_dir) if file.endswith(file_extension)]

        return self.excels_in_folder

    def load_excel_to_dataframe_dict(self, importNaN=False):
        full_file_path = os.path.join(self.extraction_folder_dir, self.file_to_extract)
        
        file_engine = self._determine_engine()

        dataframes_dict = {}
        for sheet in self.sheets_to_extract:
            df = pd.read_excel(full_file_path, sheet_name=sheet, engine=file_engine)
            
            # First drops columns that have NaN or empty string as headers, then columns where all values are NaN
            if not importNaN: 
                df = df.loc[:, df.columns.notnull()]
                df = df.loc[:, df.columns != '']
                df = df.dropna(axis=1, how='all')
                
            dataframes_dict[sheet] = df

        return dataframes_dict
        
    def get_file_sheets(self): # TODO
        # the previous old function loaded the file to dataframe to obtain the sheets it contains
            # was done through "pd.ExcelFile()" function. 
            # maybe there is another way to do so?
            #  
        pass

    def csv_to_dataframe(self):

        target_file_path = os.path.join(self.extraction_folder_dir, self.file_to_extract)
        
        # at the time, encoding, delimiter and skiprows is static...
        # todo: create way to make dynamic...

        csv_dataframe = pd.read_csv(target_file_path, encoding='utf-16', delimiter='\t', skiprows=1)

        return csv_dataframe

    def _determine_engine(self): # TODO
        file_name = self.file_to_extract

        if file_name.endswith('.xlsx') or file_name.endswith('.xlsm'):
            engine = 'openpyxl'
            # excel_file = pd.ExcelFile(file_name, engine='openpyxl')
        elif file_name.endswith('.xls'):
            engine = 'xlrd'
            # excel_file = pd.ExcelFile(file_name, engine='xlrd')
        else: # this error handling could go towards self.choose_file function
            raise ValueError("Unsupported file format. \nPlease provide a .xlsm, .xlsx, or .xls file.")
            return

        return engine

    def _detect_delimiter(self): # TODO
        # delimiters = [',', ';', '\\', '\t'] 
        pass
    
    def _detect_encoding(self): # TODO
        # encodings = ['utf-8', 'utf-8-sig', 'utf-16', 'latin1', 'iso-8859-1', 'cp1252']
        pass

    def _detect_headers(self): # TODO
        # used for the skiprows parameter in some functions (csv_to_dataframe)
        pass