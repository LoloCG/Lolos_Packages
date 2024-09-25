import pandas as pd

def identify_column_hierarchy(df): # ????
    cat_cols = []
    Num_col = None
    num_uniq_val = 0
    first_hier_col = None

    for colname in df:
        coltype = str(df[colname].dtype)
        if coltype == 'object': 
            cat_cols.append(colname)

            if df[colname].value_counts().mean() > num_uniq_val:
                
                num_uniq_val = df[colname].value_counts().mean()
                first_hier_col = colname

        elif coltype in ['float64','int64']:
            Num_col = colname

    # #print(f"Category columns: {list(cat_cols)}")
    # #print(f"Numerical columns: {Num_col}")
    # print(f"Categorical columm with highest hierarchy: {first_hier_col}")
    # #categ_in_highest_hierarch = list(df[first_hier_col].unique())
    # #print(f"Categories: {categ_in_highest_hierarch[0]}, {categ_in_highest_hierarch[1]}")

    self.highest_hierarchy_column = first_hier_col        
    self.categorical_columns = cat_cols
    self.numerical_columns = Num_col