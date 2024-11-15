import streamlit as st
import yfinance as yf
import pandas as pd
import altair as alt
import plotly.graph_objs as go

# Streamlit page settings
st.set_page_config(
    page_title="Comprehensive Stock Analysis Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar inputs
st.sidebar.header("Options")
ticker = st.sidebar.text_input("Stock Symbol", "AAPL")
fetch_data = st.sidebar.button("Fetch Data")

# Function to fetch stock data using yfinance
@st.cache_data
def fetch_stock_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        return {
            "info": stock.info,
            "history": stock.history(period="1y")
        }
    except Exception as e:
        st.error(f"Error fetching data with yfinance: {e}")
        return None

# Display Company Overview
def display_company_overview(info):
    st.header("Company Overview")
    st.subheader(info.get("shortName", "N/A"))
    st.write(info.get("longBusinessSummary", "N/A"))

# Display Key Financial Ratios using Altair bar chart
def display_key_financial_ratios(info):
    st.subheader("Key Financial Ratios")
    
    financial_ratios = {
        "P/E Ratio": info.get("trailingPE", 0),
        "P/B Ratio": info.get("priceToBook", 0),
        "EPS": info.get("trailingEps", 0),
        "Dividend Yield": info.get("dividendYield", 0),
        "Profit Margin": info.get("profitMargins", 0),
        "ROE": info.get("returnOnEquity", 0),
    }
    
    # Convert to DataFrame
    ratios_df = pd.DataFrame(list(financial_ratios.items()), columns=["Metric", "Value"])

    # Create Altair chart
    bar_chart = alt.Chart(ratios_df).mark_bar().encode(
        x=alt.X("Metric", sort=None),
        y="Value",
        tooltip=["Metric", "Value"]
    ).properties(
        width=600,
        height=400,
        title="Key Financial Ratios"
    )
    
    st.altair_chart(bar_chart)

# Display Growth Metrics
def display_growth_metrics(info):
    st.subheader("Growth Metrics")
    
    growth_metrics = {
        "Revenue Growth (3Y)": info.get("revenueGrowth", "N/A"),
        "Earnings Growth (3Y)": info.get("earningsGrowth", "N/A"),
    }
    
    growth_df = pd.DataFrame(list(growth_metrics.items()), columns=["Metric", "Value"])
    st.table(growth_df)

# Display interactive stock price chart with
