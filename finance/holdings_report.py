# Import Library
import pandas as pd

# Import Local Library
import finance.config as config
from finance.api.stock_price_api import StockPriceApi
from finance.api.mf_price_api import MfPriceApi

class HoldingsReport():
    def __init__(self):
        self.holdings_df = pd.read_csv()