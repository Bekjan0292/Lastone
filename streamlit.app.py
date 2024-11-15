import streamlit as st
import yfinance as yf
import pandas as pd
from streamlit_echarts import st_echarts
from st_aggrid import AgGrid, GridOptionsBuilder
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

# Display Key Financial Ratios using streamlit-echarts radar chart
def display_key_financial_ratios(info):
    st.subheader("Key Financial Ratios")
    
    # Financial Ratios
    financial_ratios = {
        "P/E Ratio": info.get("trailingPE", 0),
        "P/B Ratio": info.get("priceToBook", 0),
        "EPS": info.get("trailingEps", 0),
        "Dividend Yield": info.get("dividendYield", 0),
        "Profit Margin": info.get("profitMargins", 0),
        "ROE": info.get("returnOnEquity", 0),
    }

    radar_option = {
        "title": {"text": "Financial Ratios"},
        "radar": {
            "indicator": [
                {"name": "P/E Ratio", "max": 50},
                {"name": "P/B Ratio", "max": 10},
                {"name": "EPS", "max": 10},
                {"name": "Dividend Yield", "max": 5},
                {"name": "Profit Margin", "max": 1},
                {"name": "ROE", "max": 1},
            ]
        },
        "series": [{
            "name": "Financial Ratios",
            "type": "radar",
            "data": [{"value": list(financial_ratios.values()), "name": "Ratios"}]
        }]
    }

    st_echarts(radar_option, height="400px")

# Display Growth Metrics
def display_growth_metrics(info):
    st.subheader("Growth Metrics")
    
    growth_metrics = {
        "Revenue Growth (3Y)": info.get("revenueGrowth", "N/A"),
        "Earnings Growth (3Y)": info.get("earningsGrowth", "N/A"),
    }
    
    growth_df = pd.DataFrame(list(growth_metrics.items()), columns=["Metric", "Value"])
    st.table(growth_df)

# Display Profitability Ratios
def display_profitability_ratios(info):
    st.subheader("Profitability Ratios")
    
    profitability_ratios = {
        "Return on Assets (ROA)": info.get("returnOnAssets", "N/A"),
        "Return on Equity (ROE)": info.get("returnOnEquity", "N/A"),
        "Profit Margin": info.get("profitMargins", "N/A"),
    }
    
    profitability_df = pd.DataFrame(list(profitability_ratios.items()), columns=["Metric", "Value"])
    st.table(profitability_df)

# Display Liquidity Ratios
def display_liquidity_ratios(info):
    st.subheader("Liquidity Ratios")
    
    liquidity_ratios = {
        "Current Ratio": info.get("currentRatio", "N/A"),
        "Quick Ratio": info.get("quickRatio", "N/A"),
    }
    
    liquidity_df = pd.DataFrame(list(liquidity_ratios.items()), columns=["Metric", "Value"])
    st.table(liquidity_df)

# Display Leverage Ratios
def display_leverage_ratios(info):
    st.subheader("Leverage Ratios")
    
    leverage_ratios = {
        "Debt to Equity Ratio": info.get("debtToEquity", "N/A"),
        "Interest Coverage Ratio": info.get("interestCoverage", "N/A"),
    }
    
    leverage_df = pd.DataFrame(list(leverage_ratios.items()), columns=["Metric", "Value"])
    st.table(leverage_df)

# Display interactive stock price chart with Plotly
def display_stock_chart(history, ticker):
    st.subheader("Stock Price Chart")
    
    if history.empty:
        st.error("No stock data available for the selected ticker.")
        return

    fig = go.Figure(data=[go.Candlestick(
        x=history.index,
        open=history["Open"],
        high=history["High"],
        low=history["Low"],
        close=history["Close"],
        increasing_line_color="green",
        decreasing_line_color="red"
    )])
    fig.update_layout(
        title=f"{ticker.upper()} Stock Price (1 Year)",
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        xaxis_rangeslider_visible=True
    )
    st.plotly_chart(fig)

# Main App
def main():
    st.title("Comprehensive Stock Analysis Dashboard")

    if fetch_data:
        st.subheader(f"Analyzing {ticker.upper()} Data")
        stock_data = fetch_stock_data(ticker)

        if stock_data:
            info = stock_data["info"]
            history = stock_data["history"]

            # Display different sections for a comprehensive analysis
            display_company_overview(info)
            display_key_financial_ratios(info)
            display_growth_metrics(info)
            display_profitability_ratios(info)
            display_liquidity_ratios(info)
            display_leverage_ratios(info)
            display_stock_chart(history, ticker)
        else:
            st.error("Failed to fetch data. Please check the ticker symbol and try again.")

if __name__ == "__main__":
    main()
