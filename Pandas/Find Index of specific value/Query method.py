# query method lets you specify a condition as a string, and it filters the DataFrame based on this condition

import pandas as pd

# Create the DataFrame
data = {'column1': [5, 10, 15, 20, 25]}
df = pd.DataFrame(data)

# Specify the target value
target_value = 15
print("target_value =", target_value)

# Use query to find the index
target_value_index = df.query('column1 == @target_value')
    # filters the DataFrame and returns a new DataFrame that only includes rows where the condition is True.abs 
        # The result is a DataFrame that contains only the rows matching the condition.
    # 'column1 == @target_value'
        # This condition checks where column1 is equal to the value stored in target_value.
    # The @ symbol is used to refer to the variable target_value from the surrounding scope.

if not target_value_index.empty:
    index_of_target = target_value_index.index[0]
    print("Index of the target value:", index_of_target)
    print(data)
else:
    print("Target value not found.")
print("----------")

greater_than_columns = df.query('column1 > 10 and column1 < 25')
print("rows where column1 is > 10 and <25:",greater_than_columns)