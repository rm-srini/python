# Import Local Library
import finance.config as config
from stock_price_api import StockPriceApi

screener_report = [
    'Symbol',
    'Quantity',
    'AvgPrice',
    'TotalCost',
    'CurrentPrice',
    'CurrentValue',
    'PNL',
    'PortfolioWeight',
    'Sector',
    'BookValue',
    'StockPE',
    'DividendYield',
    'FaceValue',
    'High',
    'Low',
    'MarketCap',
    'ROCE',
    'ROE'
]


class ProcessReports:
    def __init__(self, holdings_df, report_type):
        self.holdings_df = holdings_df
        self.report_type = report_type
        self.target_path = config.target_path

    def process_reports(self):
        if self.report_type == 'Screener':
            self.screener_report()

    def screener_report(self):
        self.holdings_df = self.holdings_df[self.holdings_df['Segment'] == 'EQ']
        instruments = self.holdings_df.Symbol.unique()
        ratio_df = StockPriceApi(instruments).instrument_ratios()
        report = self.holdings_df.merge(ratio_df, on='Symbol', how='inner')
        report['CurrentValue'] = report['Quantity'] * report['CurrentPrice']
        report['PNL'] = report['CurrentValue'] - report['TotalCost']
        report['PortfolioWeight'] = (100 * report['CurrentValue'] / report['CurrentValue'].sum(axis=0)).round(decimals=2)
        report = report[screener_report]
        report.to_excel(self.target_path + '/ScreenerReport.xlsx', index=False, sheet_name='Portfolio')
