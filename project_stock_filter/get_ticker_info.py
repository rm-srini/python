# Common Libraries
import yfinance as yf
import pandas as pd

# Local Libraries
from config.config import stock_attribute


class GetTickerInfo:
    def __init__(self):
        self.stock_info = stock_attribute

    def get_ticker_info(self, ticker: str):
        stock = yf.Ticker(ticker)
        dic_stock_info = ({key: stock.info[key] if key in list(stock.info.keys()) else None
                           for key in self.stock_info})
        return pd.DataFrame(dic_stock_info, index=[stock.info['symbol']])

    def get_hist_price(self, ticker: str):
        stock = yf.Ticker(ticker)
        return stock.history(period="max")


if __name__ == "__main__":
    a = GetTickerInfo()
    print(a.get_ticker_info("INE738I01010"))
    print(a.get_hist_price("INE738I01010"))
