# Common Libraries
import yfinance as yf
import pandas as pd


class GetStockInfo:
    def __init__(self):
        self.stock_info = ['regularMarketPreviousClose', 'regularMarketDayLow', 'regularMarketDayHigh', 'beta',
                           'trailingPE', 'forwardPE', 'volume', 'marketCap', 'fiftyTwoWeekLow', 'regularMarketOpen',
                           'fiftyTwoWeekHigh', 'fiveYearAvgDividendYield', 'priceToSalesTrailing12Months',
                           'fiftyDayAverage', 'twoHundredDayAverage', 'profitMargins', 'floatShares',
                           'sharesOutstanding', 'bookValue', 'priceToBook', 'earningsQuarterlyGrowth',
                           'targetHighPrice', 'targetLowPrice', 'targetMeanPrice', 'targetMedianPrice',
                           'recommendationMean', 'totalDebt', 'returnOnEquity', 'earningsGrowth',
                           'revenueGrowth', 'trailingEps', 'forwardEps', 'trailingPegRatio']

    def get_stock_info(self, ticker: str):
        stock = yf.Ticker(ticker)
        dic_stock_info = ({key: stock.info[key] if key in list(stock.info.keys()) else None
                           for key in self.stock_info})
        return pd.DataFrame(dic_stock_info, index=[stock.info['symbol']])

    def get_hist_price(self, ticker: str):
        stock = yf.Ticker(ticker)
        return stock.history(period="max")


if __name__ == "__main__":
    a = GetStockInfo()
    print(a.get_stock_info("EQUITASBNK.NS"))
    print(a.get_hist_price("EQUITASBNK.NS"))
