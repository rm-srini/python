import json
import pandas as pd

# Opening JSON file
f = open('file.json')

# returns JSON object as a dictionary
data = json.load(f)
df = pd.json_normalize(data)
df_students = pd.json_normalize(data,
                                record_path='students',
                                meta=['class', 'room', ['info', 'teachers', 'math'], ['info', 'teachers', 'physics']],
                                errors='ignore',
                                sep=' | ',
                                meta_prefix='base | ',
                                record_prefix='student | ')
print(df_students)
