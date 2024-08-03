# Common Libraries
import pandas as pd
import os

# Local Libraries


class ProcessTransaction:
    def __init__(self):
        self.directory = r'data'
        self.df_tran = pd.DataFrame()

    def calculate_holdings(self,):
        holdings ={}
        start_date = self.df_tran['order_execution_time'].min().date()
        end_date = self.df_tran['order_execution_time'].max().date()
        date_range = pd.date_range(start=start_date, end=end_date)
        for date in date_range:
            pass


    def main(self):
        for filename in os.listdir(self.directory):
            file_path = os.path.join(self.directory, filename)
            if os.path.isfile(file_path):
                self.df_tran = pd.concat([self.df_tran, pd.read_csv(file_path)]) if self.df_tran.shape[0] > 0 \
                                         else pd.read_csv(file_path)
                self.df_tran['order_execution_time'] = pd.to_datetime(self.df_tran['order_execution_time'])
                self.df_tran = self.df_tran[self.df_tran['symbol'] == 'JUBLFOOD']
                self.df_tran = self.df_tran.sort_values(by='order_execution_time')
                #self.df_tran.reset_index(inplace=True)
        print(self.df_tran)


if __name__ == "__main__":
    a = ProcessTransaction()
    a.main()
    a.calculate_holdings()
