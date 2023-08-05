import time
import requests
from ehp import *
import pandas as pd
import threading

import finance.config as config



class StockPriceApi:
    def __init__(self, symbol: list):
        self.symbol = symbol
        self.tran_df = pd.DataFrame()

    def api_call(self, symbol, is_consolidated):
        print('Fetching price:{symbol} ', symbol)
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
        for sec in dom.find('p', ('class', 'sub')):
            for i in range(100):
                for val in sec.find('a', ('href', '/company/compare/000000{num}/'.format(num=str(i).zfill(2)))):
                    keys.append('Sector')
                    values.append(val.text().strip())
        return dict(zip(keys, values))

    def instrument_ratios(self) -> pd.DataFrame:
        print('Fetching Stock Price from Screener')
        print(time.ctime(time.time()))
        ratio_df = pd.DataFrame()
        for symbol in self.symbol:
            if symbol not in config.exclude_symbol:
                # dic = self.api_call(symbol, True)
                threading.Thread(target=self.api_call, args=(symbol, True,)).start()
                dic = threading.Thread.join()
                # if dic['Current Price'] == '':
                #     dic = self.api_call(symbol, False)
                ratio_df = pd.concat([ratio_df, pd.DataFrame.from_dict([dic])])
        ratio_df = ratio_df[ratio_df['Current Price'] != '']
        ratio_df = ratio_df[ratio_df['Current Price'].notnull()]
        ratio_df['BookValue'] = ratio_df['Book Value'].str.replace(',', '').astype(float).round(decimals=2)
        ratio_df['CurrentPrice'] = ratio_df['Current Price'].str.replace(',', '').astype(float).round(decimals=2)
        ratio_df['DividendYield'] = ratio_df['Dividend Yield'].str.replace(',', '').astype(float).round(decimals=2)
        ratio_df['FaceValue'] = ratio_df['Face Value'].str.replace(',', '').astype(float).round(decimals=2)
        ratio_df['High'] = ratio_df['High'].str.replace(',', '').astype(float).round(decimals=2)
        ratio_df['Low'] = ratio_df['Low'].str.replace(',', '').astype(float).round(decimals=2)
        ratio_df['MarketCap'] = ratio_df['Market Cap'].str.replace(',', '').astype(float).round(decimals=2)
        ratio_df['StockPE'] = ratio_df['Stock P/E'].str.replace(',', '').astype(float).round(decimals=2)
        ratio_df['ROCE'] = ratio_df['ROCE'].str.replace(',', '').astype(float).round(decimals=2)
        ratio_df['ROE'] = ratio_df['ROE'].str.replace(',', '').astype(float).round(decimals=2)
        ratio_df.drop(['Book Value', 'Current Price', 'Dividend Yield', 'Market Cap', 'Stock P/E', 'Face Value'], axis=1, inplace=True)
        print(time.ctime(time.time()))
        return ratio_df

ls = ['AFFLE', 'ASIANPAINT', 'ASTRAL', 'CAMS', 'CROMPTON', 'DEEPAKNTR', 'DIVISLAB', 'EQUITAS', 'GHCL'
, 'HDFCBANK', 'HDFCLIFE', 'HINDUNILVR', 'INFY', 'JUBLFOOD', 'LALPATHLAB', 'MARICO', 'PIDILITIND', 'RELAXO', 'SUNPHARMA']
StockPriceApi(ls).instrument_ratios()

#
# import time
#
#
# # create list [0, 1, ..., 9] as argument list
# list_args = range(10)
#
# # Code to execute in an independent thread
# def countdown(n):
#     print('Start T-minus', n, time.ctime(time.time()))
#     time.sleep(5)
#     print('\n End T-minus', n, time.ctime(time.time()))
#
# if __name__ == '__main__':
#     threads = []
#     print(time.ctime(time.time()))
#     # create threads
#
#
#     #
#     # # start threads
#     # for thread in threads:
#     #     print("start")
#     #     thread.start()
#
#     # join threads (let main thread wait until all other threads ended)
#     for thread in threads:
#         thread.join()
#     print(time.ctime(time.time()))
#     print("finished!")
