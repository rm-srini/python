column_mapping = {
    'symbol': 'Symbol',
    'isin': 'Isin',
    'trade_date': 'TradeDate',
    'exchange': 'Exchange',
    'segment': 'Segment',
    'series': 'Series',
    'trade_type': 'TradeType',
    'quantity': 'Quantity',
    'price': 'Price',
    'trade_id': 'TradeId',
    'order_id': 'OrderId',
    'order_execution_time': 'OrderExecTime'
}

position_converter = {
    'Symbol': 'object', 'Quantity': 'float64', 'BuyDate': 'object', 'BuyTime': 'object', 'BuyPrice': 'float64',
    'SellDate': 'object', 'SellTime': 'object', 'SellPrice': 'float', 'Profit': 'float'
}

position_columns = ['Symbol', 'Quantity', 'BuyDate', 'BuyTime', 'BuyPrice',
                    'SellDate', 'SellTime', 'SellPrice', 'Profit']

exclude_symbol = ['MAFANG', 'MON100', 'NIFTYBEES', 'GOLDBEES', 'SGBJAN30IX-GB']

source_file_path = r'C:\Users\rmsri_fk3ty4y\Downloads'

source_file_name = r'tradebook-YAA163-EQ*.csv'

target_path = r'C:\Srini\Finance'

holdings_col_order = ['Symbol', 'Quantity', 'AvgPrice', 'InvestedAmount', 'CurrentPrice', 'CurrentValue', 'PNL',
        'BookValue', 'StockPE', 'DividendYield', 'FaceValue', 'High', 'Low', 'MarketCap', 'ROCE',
       'ROE' ]
