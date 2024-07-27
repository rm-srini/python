import pandas as pd
import numpy as np

dic_emp = {
    "Name": ['Srini', 'Sai', 'Logu', 'Karthik'],
    "Company": ['BNP', 'Tiger Analytics', 'Accenture', 'BNY'],
    "Salary": [10000, 12000, None, 10500],
    "Technology": ["Data Engineer", "Data Engineer", None, "Reporting"],

}
dic_tech = {
    "TechName": ["Data Engineer", "Reporting"],
    "Description": ['Ingest files from upstream', 'Creates Reports']
}

df_emp = pd.DataFrame.from_dict(dic_emp)
print(df_emp.loc[(df_emp["Company"] == "BNP") & (df_emp['Technology'] == 'Data Engineer')])

df_tech = pd.DataFrame(dic_tech)

print(df_emp.merge(df_tech, left_on='Technology', right_on='TechName', how='left'))

print(pd.concat([df_emp, df_tech], axis=1))

print(df_emp.interpolate(method='linear'))


for k, v in dic_tech.items():
    print(k, v)

for i, row in df_emp.iterrows():
    print(i, row['Name'])

lst = [1,2,3,4,5,6]
print(lst[2])
for i in lst:
    print(i)

for i in range(0, len(lst)):
    print(lst[i], i)

lst.reverse()
print(lst)