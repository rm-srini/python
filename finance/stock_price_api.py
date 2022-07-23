import requests
from ehp import *
import pandas as pd


class StockPriceApi:
    def __init__(self, symbol: list):
        self.symbol = symbol
        self.tran_df = pd.DataFrame()

    def api_call(self, symbol):
        rsp = requests.get('https://www.screener.in/company/{symbol}/consolidated/'.format(symbol=symbol))
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
            dic = self.api_call(symbol)
            ratio_df = ratio_df.append(dic, ignore_index=True)
        return ratio_df
