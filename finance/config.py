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

position_columns = ['Symbol', 'Quantity', 'BuyDate', 'BuyTime', 'BuyPrice',
                    'SellDate', 'SellTime', 'SellPrice', 'Profit']

db_source = 'sqlserver_investment_dev'
source_file_path = r'C:\Users\rmsri_fk3ty4y\Downloads'
source_file_name = r'tradebook-YAA163-EQ*.csv'

target_path = r'C:\Srini\Finance'
