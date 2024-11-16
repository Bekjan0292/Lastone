import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set up page configuration
st.set_page_config(
    page_title="Stock Analyzer",
    page_icon="📊",
    layout="wide"
)

# Caching data using @st.cache_data
@st.cache_data
def get_stock_data(ticker):
    stock = yf.Ticker(ticker)
    return stock.info, stock.financials.T, stock.history(period="5y")

# Initialize session_state for ticker and current page
if "page" not in st.session_state:
    st.session_state["page"] = "Main"

if st.session_state["page"] == "Main":
    main_page()  # Your Main Page function
elif st.session_state["page"] == "Fundamental":
    fundamental_analysis_page()
elif st.session_state["page"] == "Technical":
    technical_analysis_page()  # Placeholder or another function

# Main Page
# Fundamental Analysis Page
def fundamental_analysis_page():
    st.title("Fundamental Analysis")

    # Input for stock ticker
    ticker = st.text_input("Enter Stock Ticker (e.g., AAPL, TSLA):", "AAPL")
    if not ticker:
        st.warning("Please enter a valid stock ticker.")
        return

    # Fetch stock information
    stock = yf.Ticker(ticker)
    info = stock.info

    # Display company and stock information
    st.header(f"{info.get('longName', 'Unknown Company')} ({ticker.upper()})")

    # Real-time stock data
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Current Price", value=f"${info.get('currentPrice', 'N/A'):.2f}")
        st.metric(label="Day's Change", value=f"{info.get('regularMarketChange', 0):.2f}",
                  delta=f"{info.get('regularMarketChangePercent', 0):.2f}%")
    with col2:
        st.metric(label="Previous Close", value=f"${info.get('previousClose', 'N/A'):.2f}")
        st.metric(label="Open", value=f"${info.get('open', 'N/A'):.2f}")
    with col3:
        st.metric(label="Day's Range",
                  value=f"{info.get('dayLow', 'N/A'):.2f} - {info.get('dayHigh', 'N/A'):.2f}")
        st.metric(label="52-Week Range",
                  value=f"{info.get('fiftyTwoWeekLow', 'N/A'):.2f} - {info.get('fiftyTwoWeekHigh', 'N/A'):.2f}")

    # Additional Metrics
    st.subheader("Additional Information")
    additional_metrics = {
        "Market Cap": f"${info.get('marketCap', 'N/A'):,}",
        "Beta (5Y Monthly)": info.get('beta', 'N/A'),
        "PE Ratio (TTM)": info.get('trailingPE', 'N/A'),
        "EPS (TTM)": f"${info.get('trailingEps', 'N/A'):.2f}",
        "Volume": f"{info.get('volume', 'N/A'):,}",
        "Forward Dividend & Yield": f"{info.get('dividendRate', 'N/A')} ({info.get('dividendYield', 'N/A'):.2%})",
    }
    additional_metrics_df = pd.DataFrame(additional_metrics.items(), columns=["Metric", "Value"])
    st.table(additional_metrics_df)

    # Company Overview
    st.subheader("Company Overview")
    st.write(f"**Sector:** {info.get('sector', 'N/A')} | **Industry:** {info.get('industry', 'N/A')}")
    st.write(f"**Business Summary:** {info.get('longBusinessSummary', 'N/A')}")

    # Back button for navigation
    if st.button("Back to Main Page"):
        st.session_state["page"] = "Main"
# Technical Analysis Page (Placeholder)
def technical_analysis_page():
    st.title("Technical Analysis")
    st.write("Technical analysis functionality will be implemented here.")

    # Back button
    if st.button("Back to Main Page"):
        st.session_state["page"] = "Main"

# Navigation between pages
if st.session_state["page"] == "Main":
    main_page()
elif st.session_state["page"] == "Fundamental":
    fundamental_analysis_page()
elif st.session_state["page"] == "Technical":
    technical_analysis_page()
