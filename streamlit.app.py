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
    st.markdown(f"**Industry**: {info.get
