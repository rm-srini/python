# Import Local Library
import pandas as pd
import numpy as np

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
    'MarketCapitalization',
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
        report['MarketCapitalization'] = np.where(report['MarketCap'] < config.market_cap['SmallCap'], 'SmallCap',
                                                  np.where(report['MarketCap'] < config.market_cap['MidCap'], 'MidCap', 'LargeCap'))

        report['PortfolioWeight'] = (100 * report['CurrentValue'] / report['CurrentValue'].sum(axis=0)).round(
            decimals=2)
        report = report[screener_report]
        stats_dict = {
            'PortfolioValue': [report['CurrentValue'].sum(axis=0)],
            'PortfolioPE': [(report['CurrentValue'] * report['StockPE']).sum(axis=0) / report['CurrentValue'].sum(
                axis=0)],
            'PortfolioROCE': [(report['CurrentValue'] * report['ROCE']).sum(axis=0) / report['CurrentValue'].sum(axis=0)]
        }
        stats_df = pd.DataFrame.from_dict(stats_dict)
        writer = pd.ExcelWriter(self.target_path + '/ScreenerReport.xlsx', engine='xlsxwriter')
        stats_df.to_excel(writer, sheet_name='Summary', index=False)
        report.to_excel(writer, sheet_name='Portfolio', index=False)
        writer.save()
        writer.close()
