import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Title and Description
st.title("Fundamental Analysis Automation")
st.markdown("""
This app automates fundamental analysis by analyzing economic, industry, 
and company-specific factors. It also provides interactive visualizations 
to help you make informed investment decisions.
""")

# User Input: Stock Ticker
ticker = st.text_input("Enter Stock Ticker (e.g., AAPL, MSFT):", value="AAPL")

# Fetch Stock Data
if ticker:
    stock = yf.Ticker(ticker)
    info = stock.info
    financials = stock.financials

    # Display Key Information
    st.header(f"Company Overview: {info['shortName']}")
    st.subheader("Key Metrics")
    
    # Display Market Cap in millions
    market_cap = info['marketCap'] / 1_000_000  # Convert to millions
    st.metric("Market Cap (in millions)", f"${market_cap:,.0f}M")

    # Display P/E Ratio (TTM)
    st.metric("P/E Ratio (TTM)", info.get('trailingPE', 'N/A'))

    # Financial Statement Trends (simplified)
    st.subheader("Financial Trends")
    st.markdown("Revenue and Net Income trends over the last 4 years.")
    fig, ax = plt.subplots()
    financials.loc['Total Revenue'].plot(kind='line', label='Revenue', ax=ax)
    financials.loc['Net Income'].plot(kind='line', label='Net Income', ax=ax)
    ax.set_title("Revenue vs. Net Income")
    ax.legend()
    st.pyplot(fig)

    # Financial Ratios (simplified)
    st.subheader("Financial Ratios")
    ratios = {
        "P/E Ratio": info.get("trailingPE"),
        "Price/Book": info.get("priceToBook"),
        "Return on Equity (ROE)": info.get("returnOnEquity"),
        "Debt/Equity": info.get("debtToEquity"),
    }
    st.write(pd.DataFrame(ratios.items(), columns=["Ratio", "Value"]))

else:
    st.info("Please enter a stock ticker to begin analysis.")
