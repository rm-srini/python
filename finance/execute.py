# Import Library
import pandas as pd
import os

# Import Local Library
from load_transactions import LoadTransaction
from calculate_position import CalculatePosition
from calculate_holdings import CalculateHoldings
from process_reports import ProcessReports
from config import target_path

class Execute:
    def __init__(self, segments, process_type):
        """
        This is the control class file which helps you to process the Equity / MutualFunds
        transactions and calculate position, holdings, capital gain and reports out of the
        transactions
        :param segments: List of Segments to be processed, namely
                                -EQ
                                -MF
        :param process_type: List of process to be executed, namely
                                -Transaction
                                -Position
                                -Holdings
                                -ScreenerReport
                                -TickerTapeReport
                                -CapitalGain
        """
        self.segments = segments
        self.process_type = process_type

    def process(self):
        if 'Transaction' in self.process_type:
            for segment in self.segments:
                LoadTransaction(segment).process_transaction()

        if 'Position' in self.process_type:
            file = target_path + '/Transaction.xlsx'
            if os.path.exists(file):
                transaction_df = pd.read_excel(file)
                CalculatePosition(transaction_df).calculate_position()
            else:
                raise Exception("Transaction File doesn't exists, please process Transaction and then generate Position")

        if 'Holdings' in self.process_type:
            file = target_path + '/Position.xlsx'
            if os.path.exists(file):
                position_df = pd.read_excel(file)
                CalculateHoldings(position_df).current_holdings()
            else:
                raise Exception("Position File doesn't exists, please process Position and then generate Holdings")

        if 'Report' in self.process_type:
            file = target_path + '/Holdings_RAW.xlsx'
            if os.path.exists(file):
                holdings_df = pd.read_excel(file)
                ProcessReports(holdings_df).process_reports()
            else:
                raise Exception("Holdings_RAW File doesn't exists, please process Holdings and then generate Report")

v_segments = ['EQ','MF']
v_process_type = [
    'Transaction',
    'Position',
    'Holdings',
    'Report'
]
Execute(segments=v_segments, process_type=v_process_type).process()
