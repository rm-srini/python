# Import Library
import pandas as pd
import os
import glob
import datetime as dt
import numpy as np
from operator import itemgetter

# Import Local Library
import finance.config as config

column_mapping = {
    'symbol': 'Symbol',
    'isin': 'Isin',
    'trade_date': 'TradeDate',
    'exchange': 'Exchange',
    'segment': 'Segment',
    'series': 'Series',
    'trade_type': 'TradeType',
    'quantity': 'Quantity',
    'price': 'Price',
    'trade_id': 'TradeId',
    'order_id': 'OrderId',
    'order_execution_time': 'OrderExecTime'
}

dtype = {
    'Symbol': object,
    'Isin': object,
    'TradeDate': np.datetime64,
    'Exchange': object,
    'Segment': object,
    'Series': object,
    'TradeType': object,
    'Quantity': float,
    'Price': float,
    'TradeId': int,
    'OrderId': int,
    'OrderExecTime': np.datetime64
}


class LoadTransaction:
    def __init__(self, segment='EQ'):
        self.file_path = config.source_file_path
        self.file_name = 'tradebook-*-MF*.csv' if segment == 'MF' else 'tradebook-*-EQ*.csv'
        self.target_path = config.target_path

    def get_latest_transaction(self) -> pd.DataFrame:
        file = self.get_latest_file()
        if not file:
            raise Exception("Transaction file not available")
        df = pd.read_csv(file)
        df.rename(column_mapping, inplace=True, axis=1)
        df = df.astype(dtype)
        return df

    def get_latest_file(self) -> list:
        files = []
        all_files = glob.glob(self.file_path + '/' + self.file_name)
        for file in all_files:
            mdt = dt.datetime.utcfromtimestamp(os.stat(file).st_mtime)
            files.append({'file_name': file, 'md_time': mdt})
        return sorted(files, key=itemgetter('md_time'), reverse=True)[0]['file_name'] if len(files) > 0 else []

    def merge_transaction(self, source_df) -> pd.DataFrame:
        eqd_trans_df = self.check_target_file('Transaction.xlsx', column_mapping.values())
        eqd_trans_df = eqd_trans_df.astype(dtype)
        new_rec_df = pd.merge(eqd_trans_df, source_df, how='outer', indicator=True).query('_merge=="right_only"').drop(
            ['_merge'], axis=1)
        return pd.concat([eqd_trans_df, new_rec_df])

    def check_target_file(self, file_name, df_columns):
        if os.path.isfile(self.target_path + '/' + file_name):
            target_df = pd.read_excel(self.target_path + '/' + file_name)
        else:
            target_df = pd.DataFrame(columns=df_columns)
        return target_df

    def process_transaction(self):
        df = self.get_latest_transaction()
        df = self.merge_transaction(df)
        df.to_excel(self.target_path + '/Transaction.xlsx', index=False)
