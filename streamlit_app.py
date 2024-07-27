import streamlit as st
from finance.portfolio2.holdings_report import HoldingsReport
portfolio_df, portfolio_dict = HoldingsReport().main()


def main():

    st.dataframe(portfolio_df, hide_index=True)

if __name__ == "__main__":
    main()







