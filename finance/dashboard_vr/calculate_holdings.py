# Import Local Library
import finance.dashboard_vr.config as config


class CalculateHoldings:
    def __init__(self, position_df):
        self.position_df = position_df
        self.target_path = config.target_path

    def current_holdings(self):
        df = self.position_df[self.position_df['SellDate'].isna()][['Symbol', 'Quantity', 'BuyPrice', 'Segment']]
        df['BuyPrice'] = df['BuyPrice'] * df['Quantity']
        holdings_df = df.groupby(['Symbol', 'Segment'], as_index=False).sum(['Quantity', 'BuyPrice'])
        holdings_df['AvgPrice'] = holdings_df['BuyPrice'] / holdings_df['Quantity']
        holdings_df['TotalCost'] = holdings_df['AvgPrice'] * holdings_df['Quantity']
        holdings_df.drop(['BuyPrice'], axis=1, inplace=True)
        holdings_df = holdings_df.sort_values(by=['Segment', 'Symbol'])
        holdings_df.to_excel(self.target_path + '/Holdings_RAW.xlsx', index=False)
        return holdings_df
