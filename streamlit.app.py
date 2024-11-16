import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Stock Analyzer",
    page_icon="📊",
    layout="wide"
)

@st.cache_data
def get_stock_data(ticker):
    stock = yf.Ticker(ticker)
    return stock.info, stock.financials.T, stock.history(period="5y")

if "ticker" not in st.session_state:
    st.session_state["ticker"] = ""
if "page" not in st.session_state:
    st.session_state["page"] = "Main"
if "stock_data" not in st.session_state:
    st.session_state["stock_data"] = None

def main_page():
    st.title("Stock Analyzer")
    ticker = st.text_input("Enter Stock Ticker (e.g., AAPL, TSLA):", value=st.session_state["ticker"])
    st.session_state["ticker"] = ticker

    if st.button("Go to Fundamental Analysis") and ticker:
        info, financials, history = get_stock_data(ticker)
        st.session_state["stock_data"] = {"info": info, "financials": financials, "history": history}
        st.session_state["page"] = "Fundamental"

def fundamental_analysis_page():
    st.title("Fundamental Analysis")
    if not st.session_state["stock_data"]:
        st.warning("Please enter a stock ticker on the main page.")
        return

    data = st.session_state["stock_data"]
    info = data["info"]
    financials = data["financials"]

    st.subheader(f"Company: {info.get('longName', 'Unknown')}")
    st.write(f"**Sector:** {info.get('sector', 'N/A')} | **Industry:** {info.get('industry', 'N/A')}")

    st.subheader("Key Metrics")
    metrics = {
        "Market Cap": f"${info.get('marketCap', 0):,}",
        "PE Ratio": info.get('forwardPE', 'N/A'),
        "Dividend Yield": f"{info.get('dividendYield', 0) * 100:.2f}%"
    }
    st.table(pd.DataFrame(metrics.items(), columns=["Metric", "Value"]))

    if st.button("Back to Main Page"):
        st.session_state["page"] = "Main"

if st.session_state["page"] == "Main":
    main_page()
elif st.session_state["page"] == "Fundamental":
    fundamental_analysis_page()
