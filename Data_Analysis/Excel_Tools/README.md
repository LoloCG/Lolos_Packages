# Examples
Importing a csv file:

    chosen_file = 'example_file.csv'
    target_folder = r'C:\Users\User\Desktop'

    input_csv = ExcelImporter()
    input_csv.add_extraction_folder(target_folder)
    df = input_csv.add_file(chosen_file).csv_to_dataframe()
    
Basic data cleaning of dataframe, with data_cleaning_utils.py module:

    cleaner = DFCleaner(df_raw)

    new_columns = ['col1', 'col2', 'col3']
    cleaner.split_column(
        column='originalcolumn', 
        separator='\\', 
        new_columns=new_columns, 
        expand=True, 
        drop_old=True)

    cleaner.normalize_column_strings(column='Subject', headers=True, items=True)
    cleaner.convert_df_dates(date_column='date_column', single_col=False)
    cleaner.replace_comma_to_dot(column='float_column')
    
    final_df = cleaner.dataframe