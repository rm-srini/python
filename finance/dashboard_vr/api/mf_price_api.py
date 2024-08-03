# Import external Library
import requests
import pandas as pd

# Import internal Library
from finance.dashboard_vr.api.mf_reference import mf_api_map
from finance.dashboard_vr.config import etf_maping

class MfPriceApi:
    def __init__(self, symbols: list):
        self.symbols = symbols
        self.mf_api_map_df = pd.json_normalize(mf_api_map)
        self.tran_df = pd.DataFrame()
        self.schemes_dict = {}

    def get_api_url(self, symbols, instrument='mf'):
        if instrument == 'mf':
            for symbol in symbols:
                fund = symbol[0: symbol.index(' - ')]
                api_df = self.mf_api_map_df[self.mf_api_map_df['schemeName'].str.upper().str.contains(fund)]
                api_df = api_df[api_df['schemeName'].str.upper().str.contains('- DIRECT')]
                api_df = api_df[api_df['schemeName'].str.upper().str.contains('- GROWTH')]
                self.schemes_dict[symbol] = 'https://api.mfapi.in/mf/' + api_df['schemeCode'].to_string(index=False)
        elif instrument == 'etf':
            for key, val in symbols.items():
                api_df = self.mf_api_map_df[self.mf_api_map_df['schemeName'] == val]
                self.schemes_dict[key] = 'https://api.mfapi.in/mf/' + api_df['schemeCode'].to_string(index=False)
        return self.schemes_dict

    def api_cal(self):
        print('Fetching mutual fund NAV')
        self.get_api_url(self.symbols, 'mf')
        self.get_api_url(etf_maping, 'etf')
        nav_dict = {'Symbol': [], 'CurrentPrice': []}
        for key, val in self.schemes_dict.items():
            rsp = requests.get(val)
            if rsp.status_code == 200:
                nav_dict["Symbol"].append(key)
                nav_dict["CurrentPrice"].append(float(pd.json_normalize(rsp.json(), record_path='data')[:1].nav.to_string(index=False)))
        return pd.DataFrame(nav_dict)







