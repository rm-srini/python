import requests
from ehp import *
import pandas as pd
import config


class StockPriceApi:
    def __init__(self, symbol: list):
        self.symbol = symbol
        self.tran_df = pd.DataFrame()

    def api_call(self, symbol, is_consolidated):
        if is_consolidated == True:
            rsp = requests.get('https://www.screener.in/company/{symbol}/consolidated/'.format(symbol=symbol))
        elif is_consolidated == False:
            rsp = requests.get('https://www.screener.in/company/{symbol}/'.format(symbol=symbol))
        keys = ['Symbol']
        values = [symbol]
        html = Html()
        dom = html.feed(rsp.content.decode('unicode_escape'))
        for ind in dom.find('li', ('class', 'flex flex-space-between')):
            for name in ind.find('span', ('class', 'name')):
                if name.text().strip() == 'High / Low':
                    keys.append('High')
                    keys.append('Low')
                else:
                    keys.append(name.text().strip())
            for val in ind.find('span', ('class', 'number')):
                values.append(val.text().strip())
        return dict(zip(keys, values))

    def instrument_ratios(self) -> pd.DataFrame:
        ratio_df = pd.DataFrame()
        for symbol in self.symbol:
            if symbol not in config.exclude_symbol:
                dic = self.api_call(symbol, True)
                if dic['Current Price'] == '':
                    dic = self.api_call(symbol, False)
                ratio_df = ratio_df.append(dic, ignore_index=True)
        ratio_df = ratio_df[ratio_df['Current Price'] != '']
        ratio_df = ratio_df[ratio_df['Current Price'].notnull()]
        ratio_df['BookValue'] = ratio_df['Book Value'].str.replace(',', '').astype(float)
        ratio_df['CurrentPrice'] = ratio_df['Current Price'].str.replace(',', '').astype(float)
        ratio_df['DividendYield'] = ratio_df['Dividend Yield'].str.replace(',', '').astype(float)
        ratio_df['FaceValue'] = ratio_df['Face Value'].str.replace(',', '').astype(float)
        ratio_df['High'] = ratio_df['High'].str.replace(',', '').astype(float)
        ratio_df['Low'] = ratio_df['Low'].str.replace(',', '').astype(float)
        ratio_df['MarketCap'] = ratio_df['Market Cap'].str.replace(',', '').astype(float)
        ratio_df['StockPE'] = ratio_df['Stock P/E'].str.replace(',', '').astype(float)
        ratio_df.drop(['Book Value', 'Current Price', 'Dividend Yield', 'Market Cap', 'Stock P/E', 'Face Value'], axis=1, inplace=True)
        return ratio_df
