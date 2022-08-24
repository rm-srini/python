# Import Library
import pandas as pd
import numpy as np
import os
import glob
import datetime as dt
from operator import itemgetter

# Import Local Library
import finance.config as config
from stock_price_api import StockPriceApi


class LoadTransaction:
    def __init__(self):
        self.file_path = config.source_file_path
        self.file_name = config.source_file_name
        self.target_path = config.target_path

    def get_latest_transaction(self) -> pd.DataFrame:
        file = self.get_latest_file()
        if not file:
            raise Exception("Transaction file not available")
        df = pd.read_csv(file)
        df.rename(config.column_mapping, inplace=True, axis=1)
        return df

    def get_latest_file(self) -> list:
        files = []
        all_files = glob.glob(self.file_path + '/' + self.file_name)
        for file in all_files:
            mdt = dt.datetime.utcfromtimestamp(os.stat(file).st_mtime)
            files.append({'file_name': file, 'md_time': mdt})
        return sorted(files, key=itemgetter('md_time'), reverse=True)[0]['file_name'] if len(files) > 0 else []

    def check_target_file(self, file_name, df_columns):
        if os.path.isfile(self.target_path + '/' + file_name):
            target_df = pd.read_excel(self.target_path + '/' + file_name)
        else:
            target_df = pd.DataFrame(columns=df_columns)
        return target_df

    def merge_transaction(self, source_df) -> pd.DataFrame:
        eqd_trans_df = self.check_target_file('EquityTransaction.xlsx', config.column_mapping.values())
        new_rec_df = pd.merge(eqd_trans_df, source_df, how='outer', indicator=True).query('_merge=="right_only"').drop(
            ['_merge'], axis=1)
        return pd.concat([eqd_trans_df, new_rec_df])

    def populate_position(self, instruments, transaction_df, position_df):
        for instrument in instruments:
            df = transaction_df[transaction_df['Symbol'] == instrument]
            df.sort_values('OrderExecTime')
            for index, row in df.iterrows():
                if row['TradeType'] == 'buy':
                    buy_row = pd.DataFrame({
                        'Symbol': [row[ 'Symbol']],
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
        position_df = position_df.astype(config.position_converter)
        return position_df

    def get_current_holdings(self, position_df, ratio_df):
        df = position_df[position_df['SellDate'].isna()][['Symbol', 'Quantity', 'BuyPrice']]
        df['BuyPrice'] = df['BuyPrice'] * df['Quantity']
        holdings_df = df.groupby(['Symbol'], as_index=False).sum(['Quantity', 'BuyPrice'])
        holdings_df['AvgPrice'] = holdings_df['BuyPrice'] / holdings_df['Quantity']
        holdings_df.drop(['BuyPrice'], axis=1, inplace=True)
        holdings_df = holdings_df.merge(ratio_df, on='Symbol', how='inner')
        holdings_df['InvestedAmount'] = holdings_df['Quantity'] * holdings_df['AvgPrice']
        holdings_df['CurrentValue'] = holdings_df['Quantity'] * holdings_df['CurrentPrice']
        holdings_df['PNL'] = holdings_df['CurrentValue'] - holdings_df['InvestedAmount']
        return holdings_df[config.holdings_col_order]

    def process_transaction(self):
        source_df = self.get_latest_transaction()
        transaction_df = self.merge_transaction(source_df)
        instruments = transaction_df.Symbol.unique()
        ratio_df = StockPriceApi(instruments).instrument_ratios()
        position_df = self.check_target_file('Position.xlsx', config.position_columns)
        position_df = self.populate_position(instruments, transaction_df, position_df)
        holdings_df = self.get_current_holdings(position_df, ratio_df)
        transaction_df.to_excel(self.target_path + '/EquityTransaction.xlsx')
        position_df.to_excel(self.target_path + '/Position.xlsx')
        holdings_df.to_excel(self.target_path + '/Holdings.xlsx')


a = LoadTransaction()
a.process_transaction()
