import streamlit as st
import requests
import pandas as pd
import yfinance as yf
import plotly.graph_objs as go

# Streamlit page settings
st.set_page_config(
    page_title="Interactive Stock Analysis",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS for custom theme
st.markdown("""
    <style>
        body {
            background-color: #f7f9fc;
            color: #333;
        }
        .block-container {
            padding: 2rem;
        }
        h1, h2, h3 {
            color: #2b5da4;
        }
        .stButton>button {
            background-color: #ff7f50 !important;
            color: white;
            border-radius: 5px;
        }
        .stTable {
            background-color: #ffffff;
            color: #333;
        }
    </style>
""", unsafe_allow_html=True)

# Helper function to fetch stock data from Yahoo Finance API
@st.cache_data
def fetch_stock_data(ticker, modules="assetProfile,price"):
    try:
        url = f"https://query1.finance.yahoo.com/v10/finance/quoteSummary/{ticker}?modules={modules}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad responses
        data = response.json()
        return data["quoteSummary"]["result"][0]
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None

# Sidebar inputs
st.sidebar.header("Options")
ticker = st.sidebar.text_input("Stock Symbol", "AAPL")
fetch_data = st.sidebar.button("Fetch Data")

# Display company profile
def display_company_profile(data):
    profile = data.get("assetProfile", {})
    price_data = data.get("price", {})

    st.subheader("Company Profile")
    st.metric("Sector", profile.get("sector", "N/A"))
    st.metric("Industry", profile.get("industry", "N/A"))
    st.metric("Website", profile.get("website", "N/A"))
    st.metric("Market Cap", price_data.get("marketCap", {}).get("fmt", "N/A"))

    with st.expander("About the Company"):
        st.write(profile.get("longBusinessSummary", "N/A"))

# Display financial metrics in a table
def display_financial_metrics(data):
    price_data = data.get("price", {})
    profile = data.get("assetProfile", {})
    financial_metrics = {
        "P/E Ratio": price_data.get("trailingPE", {}).get("fmt", "N/A"),
        "P/B Ratio": price_data.get("priceToBook", {}).get("fmt", "N/A"),
        "EPS": price_data.get("epsCurrentYear", {}).get("fmt", "N/A"),
        "Dividend Yield": price_data.get("dividendYield", {}).get("fmt", "N/A"),
        "Profit Margin": profile.get("profitMargins", {}).get("fmt", "N/A"),
        "Current Ratio": profile.get("currentRatio", "N/A"),
        "ROE": profile.get("returnOnEquity", {}).get("fmt", "N/A"),
    }

    st.subheader("Financial Metrics")
    metric_df = pd.DataFrame(list(financial_metrics.items()), columns=["Metric", "Value"])
    st.table(metric_df)

# Display stock price chart
def display_stock_chart(ticker):
    st.subheader("Stock Price Chart")
    try:
        stock_data = yf.download(ticker, period="1y", progress=False)
        if stock_data.empty:
            st.error("No stock data available for the selected ticker.")
            return

        fig = go.Figure(data=[go.Candlestick(
            x=stock_data.index,
            open=stock_data["Open"],
            high=stock_data["High"],
            low=stock_data["Low"],
            close=stock_data["Close"],
            increasing_line_color="green",
            decreasing_line_color="red"
        )])
        fig.update_layout(
            title=f"{ticker} Stock Price (1 Year)",
            xaxis_title="Date",
            yaxis_title="Price (USD)"
        )
        st.plotly_chart(fig)
    except Exception as e:
        st.error(f"Error displaying stock chart: {e}")

# Investment recommendation
def display_recommendation(data):
    price_data = data.get("price", {})
    pe_ratio = price_data.get("trailingPE", {}).get("raw")

    if pe_ratio is not None:
        st.subheader("Investment Recommendation")
        if pe_ratio < 15:
            st.write("**Recommendation:** Buy - Low P/E ratio may indicate undervaluation.")
        elif pe_ratio > 25:
            st.write("**Recommendation:** Sell - High P/E ratio may indicate overvaluation.")
        else:
            st.write("**Recommendation:** Hold - Fairly valued.")
    else:
        st.warning("P/E Ratio not available for recommendation.")

# Main App
def main():
    st.title("Interactive Stock Analysis")

    if fetch_data:
        st.subheader(f"Analyzing {ticker.upper()} Data")
        data = fetch_stock_data(ticker)

        if data:
            display_company_profile(data)
            display_financial_metrics(data)
            display_recommendation(data)
            display_stock_chart(ticker)
        else:
            st.error("Failed to fetch data. Please check the ticker symbol and try again.")

if __name__ == "__main__":
    main()
