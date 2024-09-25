import os
import xlsxwriter

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'TestExcel.xlsx') 

# Create an Excel workbook and add a worksheet.
workbook = xlsxwriter.Workbook(file_path)
worksheet = workbook.add_worksheet("data")

# Some sample data for the chart.
data = [
    ['Category', 'Value'],
    ['Apples', 10],
    ['Oranges', 4],
    ['Pears', 7],
    ['Bananas', 3],
]

# Write the data to the worksheet.
row = 0
col = 0
for category, value in data:
    worksheet.write(row, col, category)
    worksheet.write(row, col + 1, value)
    row += 1

# Create a chart object.
chart = workbook.add_chart({'type': 'column'})

# Configure the first series.
chart.add_series({
    'categories': '=Sheet1!$A$2:$A$5',
    'values': '=Sheet1!$B$2:$B$5',
    'name': 'Sales Data',
})

# Add a title and labels.
chart.set_title({'name': 'Fruit Sales'})
chart.set_x_axis({'name': 'Category'})
chart.set_y_axis({'name': 'Value'})

# Insert the chart into the worksheet.
worksheet.insert_chart('D2', chart)

# Close the workbook.
workbook.close()
os.startfile(file_path) # open the excel file