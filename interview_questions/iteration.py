
import pandas as pd

lst = [1, 2, 3, 4, 5]
for i in lst:
    print(i)

dic = {'A': [1,2,3,4], 'B': [5,6,7,8]}
for key, val in dic.items():
    print(key, val)

df = pd.DataFrame.from_dict(dic)
for idx, row in df.iterrows():
    print(idx, row['A'], row['B'])

dic1 = [{'A':1, 'B':5},
        {'A':2, 'B':6},
        {'A':3, 'B':7},
        {'A':4, 'B':8},]
df1 = pd.json_normalize(dic1)
df2 = pd.DataFrame.from_dict(dic1) 
print(df1)
print(df2)