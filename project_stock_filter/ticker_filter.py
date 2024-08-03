# Common Libraries
import pandas as pd

# Local Libraries
from get_ticker_info import GetTickerInfo


class TickerFilter:
    def __init__(self):
        self.get_ticker_info = GetTickerInfo()

    def filter_all_time_high(self, symbol: str, df_price_list: pd.DataFrame):
        dict = {'symbol': symbol, 'high': 0, 'count': 0}
        for idx, row in df_price_list.iterrows():
            if dict['high'] < row['High']:
                dict['high'] = row['High']
                dict['count'] += 1

        return dict

    def main(self):
        df_stock_list = pd.read_json(r'config\stock_list.json')
        for idx, row in df_stock_list.iterrows():
            df_price_list = self.get_ticker_info.get_hist_price(row['ISIN Code'])
            print(self.filter_all_time_high(row["Symbol"], df_price_list))


if __name__ == "__main__":
    a = TickerFilter()
    a.main()

