# Also called "K-Nearest Neighbors", "nearest neighbor search" or "proximity search". 
import pandas as pd

data = {
    'column1': [5, 10, 15, 20, 25]
}
df = pd.DataFrame(data)
print("data to search through:", data['column1'])

target_value = 18
print("Target value:", 18)

differences = df['column1'] - target_value # calculates the difference between each value in the column and the target value
# Result: [-13, -8, -3, 2, 7]

abs_differences = differences.abs() # converts the differences to their absolute values to measure proximity.
# Result: [13, 8, 3, 2, 7]

sorted_indices = abs_differences.argsort() # sorts the absolute differences and returns the indices that would sort the array.
# Result: [3, 2, 4, 1, 0]

closest_index = sorted_indices[0] # retrieves the index of the smallest difference, which is the closest value. The 0 indicates that you are selecting the first element from the sorted_indices array. 
# Result: 3 (index of the closest value)

closest_value = df['column1'].iloc[closest_index] # retrieves the actual value in the DataFrame at the closest index.
# Result: 20 (value at index 3)

print("closest value:", closest_value)

# All this code can be simplified like this:
closest_value = df['column1'].iloc[(df['column1'] - target_value).abs().argsort()[0]]
