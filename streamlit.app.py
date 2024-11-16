import streamlit as st
import yfinance as yf
import pandas as pd

# Set up page configuration
st.set_page_config(
    page_title="Stock Analyzer",
    page_icon="📊",
    layout="wide"
)

# Initialize session state for the stock ticker
if "ticker" not in st.session_state:
    st.session_state["ticker"] = ""

# Starting Page
def starting_page():
    st.title("Stock Analyzer")
    st.write("Welcome to the Stock Analyzer! Analyze stocks both fundamentally and technically.")

    # Input stock ticker
    ticker = st.text_input("Enter Stock Ticker (e.g., AAPL, TSLA):", value=st.session_state["ticker"])
    st.session_state["ticker"] = ticker

    # Buttons to choose analysis type
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Go to Fundamental Analysis"):
            st.session_state["page"] = "Fundamental"
    with col2:
        if st.button("Go to Technical Analysis"):
            st.session_state["page"] = "Technical"

# Fundamental Analysis Page
def fundamental_analysis():
    st.title("Fundamental Analysis")

    if "ticker" not in st.session_state or not st.session_state["ticker"]:
        st.warning("Please go back to the starting page and enter a stock ticker.")
        return

    ticker = st.session_state["ticker"]
    stock = yf.Ticker(ticker)
    info = stock.info

    # Company Details
    st.subheader(f"Company: {info.get('longName', 'Unknown')} ({ticker})")
    st.markdown(f"**Sector**: {info.get('sector', 'N/A')}")
    st.markdown(f"**Industry**: {info.get('industry', 'N/A')}")

    # Metrics Overview
    st.subheader("Key Financial Metrics")
    metrics = {
        "Market Cap": f"${info.get('marketCap', 0):,}",
        "Price to Earnings (PE) Ratio (TTM)": info.get('forwardPE', 'N/A'),
        "Dividend Yield": f"{info.get('dividendYield', 0) * 100:.2f}%",
        "52-Week High": f"${info.get('fiftyTwoWeekHigh', 'N/A')}",
        "52-Week Low": f"${info.get('fiftyTwoWeekLow', 'N/A')}"
    }
    metrics_df = pd.DataFrame(metrics.items(), columns=["Metric", "Value"])
    st.table(metrics_df)

    # Financial History Chart
    st.subheader("Revenue and Net Income (Last 5 Years)")
    try:
        financials = stock.financials.T
        income_statement = financials[["Total Revenue", "Net Income"]]
        st.line_chart(income_statement)
    except Exception:
        st.warning("Unable to fetch financial history data.")

    # Valuation Ratios Comparison
    st.subheader("Valuation Ratios Comparison")
    ratios = {
        "Current PE Ratio": info.get('forwardPE', 0),
        "Price-to-Book Ratio": info.get('priceToBook', 'N/A'),
        "PEG Ratio": info.get('pegRatio', 'N/A')
    }
    ratios_df = pd.DataFrame(ratios.items(), columns=["Ratio", "Value"])
    st.table(ratios_df)

    # Recommendation Logic
    st.subheader("Recommendation")
    recommendation = "Hold"
    if info.get("forwardPE", None):
        pe = info["forwardPE"]
        if pe < 15:
            recommendation = "Buy"
        elif pe > 25:
            recommendation = "Sell"

    st.markdown(f"### **Recommendation: {recommendation}**")

    # Navigation
    if st.button("Back to Start"):
        st.session_state["page"] = "Start"

# Technical Analysis Placeholder
def technical_analysis():
    st.title("Technical Analysis")
    st.write("Technical analysis functionality will go here.")

    # Navigation
    if st.button("Back to Start"):
        st.session_state["page"] = "Start"

# Navigation Logic
if "page" not in st.session_state:
    st.session_state["page"] = "Start"

if st.session_state["page"] == "Start":
    starting_page()
elif st.session_state["page"] == "Fundamental":
    fundamental_analysis()
elif st.session_state["page"] == "Technical":
    technical_analysis()
