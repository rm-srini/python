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
        self.eqd_trans_df = pd.DataFrame(columns=column_mapping.values())
        self.eqd_trans_df = self.eqd_trans_df.astype(dtype)

    def get_latest_transaction(self) -> pd.DataFrame:
        files = self.get_latest_file()
        lst_df = []
        if files == []:
            raise Exception("Transaction file not available")
        for file in files:
            print('Processing file: ' + file['file_name'])
            df = pd.read_csv(file['file_name'])
            df.rename(column_mapping, inplace=True, axis=1)
            df = df.astype(dtype)
            lst_df.append(df)
        return lst_df

    def get_latest_file(self) -> list:
        files = []
        all_files = glob.glob(self.file_path + '/' + self.file_name)
        for file in all_files:
            mdt = dt.datetime.utcfromtimestamp(os.stat(file).st_mtime)
            files.append({'file_name': file, 'md_time': mdt})
        return sorted(files, key=itemgetter('md_time'), reverse=False)

    def merge_transaction(self, lst_df) -> pd.DataFrame:
        self.check_target_file('Transaction.xlsx')
        self.eqd_trans_df = pd.concat(lst_df)


    def check_target_file(self, file_name):
        if os.path.isfile(self.target_path + '/' + file_name):
            os.remove(self.target_path + '/' + file_name)

    def process_transaction(self):
        lst_df = self.get_latest_transaction()
        df = self.merge_transaction(lst_df)
        self.eqd_trans_df.to_excel(self.target_path + '/Transaction.xlsx', index=False)
