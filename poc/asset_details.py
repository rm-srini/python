import pandas as pd
import numpy as np

df = pd.read_excel(r'C:\Users\rmsri_fk3ty4y\Downloads\AssetDetails.xlsx', sheet_name='Sheet4')

df_explode = df.assign(PlotNo=df['PlotNo'].str.split(',')).explode('PlotNo')
df_explode['PlotNo'] = df_explode['PlotNo'].str.strip()
df_explode['Cnt'] = df_explode.groupby("DocumentNumber")["DocumentNumber"].transform('count')
df_explode['Extent'] = df_explode['Extent'] / df_explode['Cnt']
df_explode['RegistrationValue'] = df_explode['RegistrationValue'] / df_explode['Cnt']
df_explode['InPossession'] = False
df_explode['Year'] = df_explode['DateOfRegistration'].dt.year
df_explode['InPossession'] = np.where((df_explode['Type'] == 'Buy'), True, df_explode['InPossession'])
for index, row in df_explode.iterrows():
    if row['Type'] == 'Sell':
        df_explode['InPossession'] = np.where((df_explode['PlotNo'] == row['PlotNo']) &
                                              (df_explode['Type'] == 'Buy'), False, df_explode['InPossession'])

df_explode.to_excel(r'C:\Users\rmsri_fk3ty4y\Downloads\AssetProcessed.xlsx', index=False)