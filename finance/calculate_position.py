# Import Library
import pandas as pd
import numpy as np

# Import Local Library
import finance.config as config

position_converter = {
    'Symbol': object,
    'Segment': object,
    'Quantity': float,
    'BuyDate': np.datetime64,
    'BuyTime': np.datetime64,
    'BuyPrice': float,
    'SellDate': np.datetime64,
    'SellTime': np.datetime64,
    'SellPrice': float,
    'Profit': float
}

class CalculatePosition():
    def __init__(self, transaction_df):
        self.transaction_df = transaction_df
        self.target_path = config.target_path

    def populate_position(self, instruments, transaction_df, position_df):
        for instrument in instruments:
            df = transaction_df[transaction_df['Symbol'] == instrument]
            df.sort_values('OrderExecTime')
            for index, row in df.iterrows():
                if row['TradeType'] == 'buy':
                    buy_row = pd.DataFrame({
                        'Symbol': [row['Symbol']],
                        'Segment': [row['Segment']],
                        'Quantity': [row['Quantity']],
                        'BuyDate': [row['TradeDate']],
                        'BuyTime': [row['OrderExecTime']],
                        'BuyPrice': [row['Price']]
                    })
                    position_df = pd.concat([position_df, buy_row], ignore_index=True)

                if row['TradeType'] == 'sell':
                    sr = position_df[(position_df['SellDate'].isna()) &
                           (position_df['Symbol'] == row['Symbol'])]['BuyTime'] == position_df[(position_df['SellDate'].isna()) &
                           (position_df['Symbol'] == row['Symbol'])]['BuyTime'].min()
                    idx = sr[sr==True].index[0]

                    if position_df.iloc[idx]['Quantity'] == row['Quantity']:
                        position_df.at[idx, 'SellDate'] = row['TradeDate']
                        position_df.at[idx, 'SellTime'] = row['OrderExecTime']
                        position_df.at[idx, 'SellPrice'] = row['Price']

                    elif position_df.iloc[idx]['Quantity'] > row['Quantity']:
                        dict = {
                                'Symbol': position_df.iloc[idx]['Symbol'],
                                'Segment': position_df.iloc[idx]['Segment'],
                                'Quantity': position_df.iloc[idx]['Quantity'] - row['Quantity'],
                                'BuyDate': position_df.iloc[idx]['BuyDate'],
                                'BuyTime': position_df.iloc[idx]['BuyTime'],
                                'BuyPrice': position_df.iloc[idx]['BuyPrice'],
                                'SellDate': np.NaN,
                                'SellTime': np.NaN,
                                'SellPrice': np.NaN,
                                'Profit': np.NaN
                        }
                        position_df = position_df.append(dict, ignore_index=True)
                        position_df.at[idx, 'Quantity'] = row['Quantity']
                        position_df.at[idx, 'SellDate'] = row['TradeDate']
                        position_df.at[idx, 'SellTime'] = row['OrderExecTime']
                        position_df.at[idx, 'SellPrice'] = row['Price']

                    elif position_df.iloc[idx]['Quantity'] < row['Quantity']:
                        position_df.at[idx, 'SellDate'] = row['TradeDate']
                        position_df.at[idx, 'SellTime'] = row['OrderExecTime']
                        position_df.at[idx, 'SellPrice'] = row['Price']
                        row['Quantity'] = row['Quantity'] - position_df.iloc[idx]['Quantity']
                        df_new = pd.DataFrame()
                        df_new = df_new.append(row, ignore_index=True)
                        position_df = self.populate_position([instrument], df_new, position_df)
        position_df['Profit'] = ((position_df['Quantity'] * position_df['SellPrice']) -
                                        (position_df['Quantity'] * position_df['BuyPrice']))
        position_df = position_df.astype(position_converter)
        return position_df

    def calculate_position(self):
        instruments = self.transaction_df.Symbol.unique()
        position_df = pd.DataFrame(columns=list(position_converter.keys()))
        df = self.populate_position(instruments, self.transaction_df, position_df)
        df.to_excel(self.target_path + '/Position.xlsx', index=False)
        return df
