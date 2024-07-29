import pandas as pd

# Dictionary of dataframes
df_dict_data = {
    'Series_1': pd.DataFrame({
        'X': [1, 2, 3, 4, 5],
        'Y': [10, 15, 16, 25, 30]
    }),
    'Series_2': pd.DataFrame({
        'X': [1, 2, 3, 4, 5],
        'Y': [9, 14, 18, 28, 33]
    }),
    'Series_3': pd.DataFrame({
        'X': [1, 2, 3, 4, 5],
        'Y': [9, 16, 17, 30, 35]
    })
}

df_dict = {}

for index, (key, df) in enumerate(df_dict_data.items()): 
    new_key = f'Series_{index+1}'
    df_dict[new_key] = df
    
print(type(df_dict))

# Simple Dataframe
df_data = {
    'Series1': {'X': [1, 2, 3, 4, 5], 'Y': [10, 15, 16, 25, 30]},
    'Series2': {'X': [1, 2, 3, 4, 5], 'Y': [9, 14, 18, 28, 33]},
    'Series3': {'X': [1, 2, 3, 4, 5], 'Y': [9, 16, 17, 30, 35]}
}
# df = pd.DataFrame(df_template)
