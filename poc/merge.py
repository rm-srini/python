import pandas as pd
d1 = {'col1': [1, 1 , 1, 1, 2, 3]}
d2 = {'col1': [1, 1, 2, 7, 8]}
df1 = pd.DataFrame(d1)
df2 = pd.DataFrame(d2)

inner_df = df1.merge(df2, how='inner', on='col1')
left_df = df1.merge(df2, how='left', on='col1')
right_df = df1.merge(df2, how='right', on='col1')
outer_df = df1.merge(df2, how='outer', on='col1')
print(inner_df)
