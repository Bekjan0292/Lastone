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
    balance_sheet = stock.balance_sheet
    cash_flow = stock.cashflow

    # Display Key Information
    st.header(f"Company Overview: {info['shortName']}")
    st.subheader("Summary")
    st.write(info.get('longBusinessSummary', 'No description available.'))
    
    st.subheader("Key Metrics")
    st.metric("Market Cap", f"${info['marketCap']:,}")
    st.metric("PE Ratio (TTM)", info.get('trailingPE', 'N/A'))
    st.metric("Dividend Yield", f"{info.get('dividendYield', 0) * 100:.2f}%")

    # Financial Statement Trends
    st.subheader("Financial Trends")
    st.markdown("Revenue and Net Income trends over the last 4 years.")
    fig, ax = plt.subplots()
    financials.loc['Total Revenue'].plot(kind='line', label='Revenue', ax=ax)
    financials.loc['Net Income'].plot(kind='line', label='Net Income', ax=ax)
    ax.set_title("Revenue vs. Net Income")
    ax.legend()
    st.pyplot(fig)

    # Ratio Analysis
    st.subheader("Financial Ratios")
    ratios = {
        "P/E Ratio": info.get("trailingPE"),
        "Price/Book": info.get("priceToBook"),
        "Return on Equity (ROE)": info.get("returnOnEquity"),
        "Debt/Equity": info.get("debtToEquity"),
    }
    st.write(pd.DataFrame(ratios.items(), columns=["Ratio", "Value"]))

    # Industry Comparison (Placeholder)
    st.subheader("Industry Comparison")
    st.write("Coming soon: Peer comparison within the same sector.")

    # Download Report
    if st.button("Download Report"):
        report = pd.DataFrame(ratios.items(), columns=["Ratio", "Value"])
        report.to_csv("financial_report.csv")
        st.write("Report downloaded as `financial_report.csv`.")

else:
    st.info("Please enter a stock ticker to begin analysis.")
