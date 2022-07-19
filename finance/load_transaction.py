# Import Library
import pandas as pd
import os
import glob
import time
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
        get_last_file()
        df = pd.read_csv(r'C:\Srini\Python\Finance\Feed\tradebook-YAA163-EQ.csv')
        df.rename(config.column_mapping, inplace=True, axis=1)
        self.db.insert_records(df, 'EquityTransaction')

    def get_latest_file(self) -> list:
        files = []
        dt_file = {}
        all_files = glob.glob(self.file_path + '/' + self.file_name)

        for file in all_files:
            dt_file['file_name'] = file
            dt_file['md_time'] = time.ctime( os.path.getctime(file))
            files.append(dt_file)
        return sorted(files, key=itemgetter('md_time'))




a = LoadTransaction()
file = a.get_latest_file()
print(file)