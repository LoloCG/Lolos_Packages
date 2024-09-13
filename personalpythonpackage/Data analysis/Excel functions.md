# Load Excel file into DataFrame
    file_path = 'path/to/your/input_excel_file.xlsx'
    df = pd.read_excel(file_path)

# Save DataFrame to an Excel file
    output_path = 'path/to/your/output_excel_file.xlsx'
    df.to_excel(output_path, index=False)

# Opening .csv files
    # df_dict = pd.read_csv(file_path)

# To change from "," to "." in a dataframe column:
    # dataframe['column'] = dataframe['column'].str.replace(',', '.').astype(float)

# to import a module, add the directory containing a module to sys.path, then import the module:
    import sys
    sys.path.append(r'C:\Users\Lolo\Desktop\Programming\GITRepo\PythonLearn-Resources\Data analysis\Pandas\Excel')
    module_excel_ImportExport_functs = __import__('module_excel_ImportExport_functs')

# the two following used to obtain the path of the script, then to join them with the file selected.
    main_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(main_dir, chosen_file)
