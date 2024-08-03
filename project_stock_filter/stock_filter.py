# Common Libraries
import pandas as pd

# Local Libraries
from get_stock_info import GetStockInfo


class FilterStocks:
    def __init__(self):
        self.GetStockInfo = GetStockInfo()

    def filter_all_time_high(self, symbol: str, df_price_list: pd.DataFrame):
        dict = {'symbol': symbol, 'high': 0, 'count': 0}
        for idx, row in df_price_list.iterrows():
            if dict['high'] < row['High']:
                dict['high'] = row['High']
                dict['count'] += 1

        return dict

    def iterate_stocks(self):
        df_price_list = self.GetStockInfo.get_hist_price("EQUITASBNK.NS")
        print(self.filter_all_time_high("EQUITASBNK.NS", df_price_list))


if __name__ == "__main__":
    a = FilterStocks()
    a.iterate_stocks()
