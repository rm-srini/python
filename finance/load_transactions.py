# Import Library
import pandas as pd
import os
import glob
import datetime as dt
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

class LoadTransaction:
    def __init__(self):
        self.file_path = config.source_file_path
        self.file_name = 'tradebook-*'
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

    def merge_transaction(self, source_df) -> pd.DataFrame:
        eqd_trans_df = self.check_target_file('EquityTransaction.xlsx', config.column_mapping.values())
        new_rec_df = pd.merge(eqd_trans_df, source_df, how='outer', indicator=True).query('_merge=="right_only"').drop(
            ['_merge'], axis=1)
        return pd.concat([eqd_trans_df, new_rec_df])