import streamlit as st
from finance.portfolio2.holdings_report import HoldingsReport

portfolio_df, portfolio_dict = HoldingsReport().main()

def main():
    st.dataframe(portfolio_df)

'''def main():
    st.title("Simple Greeting App")

    # Get user input for name
    name = st.text_input("Enter your name:")

    # Display the greeting message
    if name:
        st.write(f"Hello, {name}!")'''


if __name__ == "__main__":
    main()




