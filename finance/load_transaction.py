# Import Library
import pandas as pd
import os
import glob
import datetime as dt
from operator import itemgetter

# Import Local Library
from common.access_db.database import Database
import finance.config as config





class LoadTransaction:
    def __init__(self):
        self.db = Database(config.db_source)
        self.file_path = config.file_path
        self.file_name = config.file_name

    def load_eqd_transaction(self):
        file = self.get_latest_file()
        df = pd.read_csv(file)
        df.rename(config.column_mapping, inplace=True, axis=1)
        df['OrderExecTime'] = df['OrderExecTime'].dt.strftime('%Y/%m/%d %H:%M')
        self.db.insert_records(df, 'EquityTransaction')

    def get_latest_file(self) -> list:
        files = []
        all_files = glob.glob(self.file_path + '/' + self.file_name)
        for file in all_files:
            mdt = dt.datetime.utcfromtimestamp(os.stat(file).st_mtime)
            files.append({'file_name': file, 'md_time': mdt})
        return sorted(files, key=itemgetter('md_time'), reverse=True)[0]['file_name'] if len(files) > 0 else []




a = LoadTransaction()
file = a.load_eqd_transaction()
print(file)