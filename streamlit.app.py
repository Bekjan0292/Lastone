import streamlit as st

def main_page():
    st.title("Stock Analysis Application")
    st.markdown("""
    Welcome to the Stock Analysis Application! This tool helps you analyze stocks using **technical analysis** and **fundamental analysis**.

    ### What is Technical Analysis?
    - Examines historical price charts, trends, and patterns.
    - Uses tools like moving averages, RSI, and MACD to identify trading opportunities.

    ### What is Fundamental Analysis?
    - Evaluates financial health, earnings, and company metrics.
    - Focuses on valuation, growth prospects, and business fundamentals.

    Please go to the Main Page and enter a stock ticker and select the type of analysis to proceed.
    """)

