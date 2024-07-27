# Load Excel file into DataFrame
file_path = 'path/to/your/input_excel_file.xlsx'
df = pd.read_excel(file_path)

# Save DataFrame to an Excel file
output_path = 'path/to/your/output_excel_file.xlsx'
df.to_excel(output_path, index=False)

