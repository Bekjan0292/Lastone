import streamlit as st

# Title for the Glossary Page
st.title("Glossary of Financial Terms")

# Introductory Text
st.markdown("""
This glossary provides definitions and explanations for commonly used financial and stock market terms. 
Use this page as a reference to enhance your understanding of key concepts.
""")

# Search Functionality
search_term = st.text_input("Search for a term:")

# Glossary Terms and Definitions
glossary = {
    "P/E Ratio": "The price-to-earnings (P/E) ratio is a valuation metric calculated by dividing a company's stock price by its earnings per share (EPS).",
    "Market Capitalization": "The total value of a company's outstanding shares, calculated by multiplying the stock price by the number of shares.",
    "ROE": "Return on Equity (ROE) is a measure of financial performance, calculated as net income divided by shareholders' equity.",
    "Beta": "Beta is a measure of a stock's volatility relative to the overall market.",
    "Dividend Yield": "The dividend yield is the annual dividend payment divided by the stock's current price, expressed as a percentage.",
    "RSI": "The Relative Strength Index (RSI) is a momentum indicator that measures the speed and change of price movements.",
    "Moving Average": "A moving average smooths out price data to identify trends over a specific time frame."
}

# Filter Terms by Search
if search_term:
    filtered_glossary = {term: definition for term, definition in glossary.items() if search_term.lower() in term.lower()}
    if not filtered_glossary:
        st.warning("No terms found. Try searching for another term.")
else:
    filtered_glossary = glossary

# Display Glossary Terms
for term, definition in filtered_glossary.items():
    with st.expander(term):
        st.markdown(definition)
