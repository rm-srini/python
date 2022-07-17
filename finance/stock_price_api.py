import requests
from ehp import *
from pathlib import Path
import pandas as pd



class StockPriceApi:
    def __init__(self):
        self.config = config_values
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

    def ingest_transactions(self):
        files = Path((self.config['transaction_file_path'])).glob('*.xlsx')
        for file in files:
            self.tran_df = pd.read_excel(file, skiprows=10)

        print(self.tran_df)

    def symbol_ratios(self):
        symbol_df = pd.DataFrame()
        for symbol in self.config['symbol_mapping']:
            print(symbol)
            dic = self.api_call(symbol)
            symbol_df = symbol_df.append(dic, ignore_index=True)
        symbol_df.to_csv('symbol.csv')


a = PortfolioManagement()
dic = a.symbol_ratios()
print(dic)