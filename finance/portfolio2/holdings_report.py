# Import Library
import pandas as pd

# Import Local Library
from finance.load_transactions import LoadTransaction
from finance.api.stock_price_api import StockPriceApi

class HoldingsReport(LoadTransaction):
    def __init__(self):
        super().__init__()
        self.file_name = 'holdings-YAA163*.xlsx'
        self.df = pd.DataFrame()

    def load_holdings_df(self):
        lt = self.get_latest_file()
        file = lt[len(lt) - 1]['file_name']
        self.df = pd.read_excel(file, skiprows=22)
        self.df.drop(columns=self.df.columns[0], axis=1, inplace=True)
        self.calc_dict = {}


    def api_call(self):
        symbol_ls = self.df['Symbol'].tolist()
        ratio_df  = StockPriceApi(symbol_ls).instrument_ratios()
        self.df = pd.merge(self.df, ratio_df, on='Symbol')

    def claculations(self):
        self.df = self.df.rename(columns={'Symbol': 'StockName', 'Sector_x': 'Sector', 'Quantity Available': 'Quantity',
                                          'Average Price': 'AveragePrice', 'StockPE': 'PE'})
        self.df = self.df[['StockName', 'Sector', 'Quantity', 'AveragePrice', 'CurrentPrice', 'PE', 'ROCE', 'ROE',
                           'BookValue', 'DividendYield', 'FaceValue',  'High', 'Low','MarketCap']]
        self.df['BuyValue'] = self.df['AveragePrice'] * self.df['Quantity']
        self.df['CurrentValue'] = self.df['CurrentPrice'] * self.df['Quantity']
        self.df['Weightage'] = self.df['CurrentValue'] / self.df['CurrentValue'].sum()
        self.df['DividendAmount'] = self.df['CurrentValue'] * self.df['DividendYield']
        self.calc_dict['WtPE'] = (self.df['PE'] * self.df['Weightage']).sum() / self.df['Weightage'].sum()
        self.calc_dict['WtROCE'] = (self.df['ROCE'] * self.df['Weightage']).sum() / self.df['Weightage'].sum()
        self.calc_dict['WtROE'] = (self.df['ROE'] * self.df['Weightage']).sum() / self.df['Weightage'].sum()
        self.calc_dict['WtDivYield'] = (self.df['DividendYield'] * self.df['Weightage']).sum() / self.df['Weightage'].sum()


    def main(self):
        self.load_holdings_df()
        self.api_call()
        self.claculations()
        return self.df, self.calc_dict



