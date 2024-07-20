import pandas as pd

# Define file paths
file_path = 'path/to/your/input_excel_file.xlsx'
output_path = 'path/to/your/output_excel_file.xlsx'

# Load Excel file into DataFrame
df = pd.read_excel(file_path)

# Define the column for extraction and the range values
column_name = "YourColumnName"
start_value = None  # Replace with your start value if needed
end_value = "YourEndValue"  # Replace with your end value

# Extract data from the start to the end value within the specified column
if start_value is None:
    start_idx = 0
else:
    start_idx = df[df[column_name] == start_value].index[0]

if end_value is None:
    end_idx = len(df)
else:
    end_idx = df[df[column_name] == end_value].index[0] + 1  # +1 to include the end value

extracted_data = df.iloc[start_idx:end_idx]

# Create a new DataFrame with the extracted data
cleaned_df = pd.DataFrame(extracted_data)

# Save the cleaned DataFrame to an Excel file
cleaned_df.to_excel(output_path, index=False)
