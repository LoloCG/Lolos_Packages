import pandas as pd

def add_excel_scatter_chart(output_excel_path, df_dict):
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

        ''' OLD UNUSED CODE
        if sheet_name == "Averages": # Change style for Averages
            line_style['dash_type'] = 'dash'
            line_style['color'] = 'red' 
            line_style['width'] = 3
        '''


script_dir = os.path.dirname(os.path.abspath(__file__))
output_filename = "test" + '.xlsx'
output_dir = os.path.join(script_dir, output_filename)

add_excel_scatter_chart(output_dir, df_dict)

os.startfile(output_dir)
