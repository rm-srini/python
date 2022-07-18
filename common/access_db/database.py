import pyodbc
import sqlalchemy
import pandas as pd

from common.access_db.connection_details import db_source


class DB:
    def __init__(self, db_config):
        self.db_config = db_config
        self.con = sqlalchemy.create_engine(self.get_connection_str())

    def get_connection_str(self):
        server = db_source[self.db_config]['setting']['hostname']
        db = db_source[self.db_config]['setting']['database']
        driver = 'SQL Server'
        return 'mssql+pyodbc://{}/{}?driver={}'.format(server, db, driver)

    def get_query_output(self, query):
        return pd.read_sql(query, self.con)

    def insert_records(self, df, table):
        df.to_sql(table, con=self.con, if_exists='append', index_label='EquityTransactionKey')




a = DB('sqlserver_investment_dev')
mapping = {
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
    'order_id': 'OrderId'
}
df = pd.read_csv(r'C:\Srini\Python\Finance\Feed\tradebook-YAA163-EQ.csv')
df = df.rename(mapping)
a.insert_records(df, 'EquityTransaction')
