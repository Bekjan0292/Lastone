import streamlit as st
import pandas as pd

st.title("Glossary of Financial Terms")

st.markdown("""
This glossary provides definitions for commonly used financial terms in the stock market. Use the search bar to quickly find terms of interest.
""")

# Glossary Data
glossary_data = [
    {"Term": "P/E Ratio", "Definition": "Price-to-Earnings ratio. A valuation metric calculated by dividing stock price by earnings per share (EPS)."},
    {"Term": "Market Capitalization", "Definition": "The total value of a company's outstanding shares, calculated as stock price multiplied by the number of shares."},
    {"Term": "ROE", "Definition": "Return on Equity. A measure of profitability calculated as net income divided by shareholder's equity."},
    {"Term": "Beta", "Definition": "A measure of a stock's volatility compared to the market."},
    {"Term": "Dividend Yield", "Definition": "The annual dividend payment divided by the stock price, expressed as a percentage."},
    {"Term": "RSI", "Definition": "Relative Strength Index. A momentum indicator measuring the speed and change of price movements, ranging from 0 to 100."},
    {"Term": "Moving Average", "Definition": "An indicator that smooths price data to identify trends over a time period."}
]

glossary_df = pd.DataFrame(glossary_data)

search_term = st.text_input("Search for a term:")

if search_term:
    filtered_glossary = glossary_df[glossary_df["Term"].str.contains(search_term, case=False)]
else:
    filtered_glossary = glossary_df

st.dataframe(filtered_glossary, use_container_width=True)
