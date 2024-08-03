# Import Library
import pandas as pd

# Import Local Library
import config


class GenerateCapitalGain:
    def __init__(self, from_date, to_date):
        self.from_date = from_date
        self.to_date = to_date
        self.target_path = config.target_path
        self.position_file = self.target_path + '/Position.xlsx'
        self.cg_df = pd.read_excel(self.position_file)

    def classify_transaction(self):
        self.cg_df = self.cg_df[self.cg_df.SellDate.notnull()]
        print(self.cg_df)



a = GenerateCapitalGain()
a.classify_transaction()