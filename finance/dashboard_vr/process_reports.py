# Import Local Library
import pandas as pd
import numpy as np
from operator import itemgetter
import glob
import datetime as dt
import os

import finance.dashboard_vr.config as config
from finance.dashboard_vr.api.stock_price_api import StockPriceApi
from finance.dashboard_vr.api.mf_price_api import MfPriceApi


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
    def __init__(self, holdings_df):
        self.holdings_df = holdings_df
        self.target_path = config.target_path

    def process_reports(self):
        equity_df = self.equity_report()
        equity_df = equity_df[['Symbol', 'Quantity', 'AvgPrice', 'TotalCost', 'CurrentPrice', 'CurrentValue', 'PNL']]
        equity_df['Segment'] = 'EQ'
        mf_df = self.mf_report()
        consolidated_df = pd.concat([equity_df, mf_df])
        consolidated_df.to_excel(self.target_path + '/ConsolidatedReport.xlsx', index=False, sheet_name='ConsolidatedReport')

    def equity_report(self):
        holdings_df = self.holdings_df[self.holdings_df['Segment'] == 'EQ']
        instruments = holdings_df.Symbol.unique()
        # tt = self.process_tickertape_file()
        # ticker_tape_df = holdings_df.merge(tt, left_on='Symbol', right_on='Ticker', how='inner')
        # ticker_tape_df = ticker_tape_df[ticker_tape_df['Segment'] == 'EQ']
        # ticker_tape_df['CP PE'] = ticker_tape_df['AvgPrice'] / ticker_tape_df['Earnings Per Share']
        ratio_df = StockPriceApi(instruments).instrument_ratios()
        report = holdings_df.merge(ratio_df, on='Symbol', how='inner')
        report['CurrentValue'] = report['Quantity'] * report['CurrentPrice']
        report['PNL'] = report['CurrentValue'] - report['TotalCost']
        report['MarketCapitalization'] = np.where(report['MarketCap'] < config.market_cap['SmallCap'], 'SmallCap',
                                                  np.where(report['MarketCap'] < config.market_cap['MidCap'], 'MidCap', 'LargeCap'))

        report['PortfolioWeight'] = (100 * report['CurrentValue'] / report['CurrentValue'].sum(axis=0)).round(
            decimals=2)
        report = report[screener_report]
        stats_dict = {
            'PortfolioValue': [report['CurrentValue'].sum(axis=0)],
            'PortfolioCost': [report['TotalCost'].sum(axis=0)],
            'Return': [report['PNL'].sum(axis=0)],
            'PortfolioPE': [(report['CurrentValue'] * report['StockPE']).sum(axis=0) / report['CurrentValue'].sum(
                axis=0)],
            'PortfolioROCE': [(report['CurrentValue'] * report['ROCE']).sum(axis=0) / report['CurrentValue'].sum(axis=0)]
        }
        stats_df = pd.DataFrame.from_dict(stats_dict)
        writer = pd.ExcelWriter(self.target_path + '/EquityReport.xlsx', engine='xlsxwriter')
        stats_df.to_excel(writer, sheet_name='Summary', index=False)
        report.to_excel(writer, sheet_name='Portfolio', index=False)
        # ticker_tape_df.to_excel(writer, sheet_name='TickerTape', index=False)
        writer.save()
        #writer.close()
        return report

    def mf_report(self):
        holdings_df = self.holdings_df[self.holdings_df['Segment'] == 'MF']
        instruments = holdings_df.Symbol.unique()
        nav_df = MfPriceApi(instruments).api_cal()
        for key, val in config.etf_maping.items():
            etf_df = self.holdings_df[self.holdings_df['Symbol'] == key]
            etf_df = etf_df.reset_index(drop=True)
            # etf_df['Segment'] = 'ETF'
            etf_df.loc[0:, 'Segment'] = 'ETF'
            holdings_df = pd.concat([holdings_df, etf_df])
        report = holdings_df.merge(nav_df, on='Symbol', how='inner')
        report['TotalCost'] = report['Quantity'] * report['AvgPrice']
        report['CurrentValue'] = report['Quantity'] * report['CurrentPrice']
        report['PNL'] = report['CurrentValue'] - report['TotalCost']
        report.to_excel(self.target_path + '/MutualFundReport.xlsx', index=False)
        return report

    def process_tickertape_file(self):
        files = []
        all_files = glob.glob(config.source_file_path + '/' + 'New_Screen_*')
        for file in all_files:
            mdt = dt.datetime.utcfromtimestamp(os.stat(file).st_mtime)
            files.append({'file_name': file, 'md_time': mdt})
        file = sorted(files, key=itemgetter('md_time'), reverse=True)[0]['file_name'] if len(files) > 0 else []
        return pd.read_csv(file)

