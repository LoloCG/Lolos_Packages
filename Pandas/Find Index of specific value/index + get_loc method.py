# typically used to find the location of a specific index label within a DataFrame's index. 
# However, this method is not suitable for finding the location of a value within a column's values. 
    # Instead, it is used to locate positions within the index itself.

import pandas as pd

# Create the DataFrame with a custom index
data = {'column1': [5, 10, 15, 20, 25]}
df = pd.DataFrame(data, index=['a', 'b', 'c', 'd', 'e'])

# Specify the target index label
target_index_label = 'c'

# Find the location of the target index label
index_position = df.index.get_loc(target_index_label)

print("Position of the target index label:", index_position)
