import streamlit as st
import yfinance as yf
import pandas as pd
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

# Display company profile
def display_company_profile(info):
    st.subheader("Company Profile")
    st.metric("Sector", info.get("sector", "N/A"))
    st.metric("Industry", info.get("industry", "N/A"))
    st.metric("Website", info.get("website", "N/A"))
    st.metric("Market Cap", f"${info.get('marketCap', 'N/A'):,}" if info.get("marketCap") else "N/A")

    with st.expander("About the Company"):
        st.write(info.get("longBusinessSummary", "N/A"))

# Display financial metrics in a table
def display_financial_metrics(info):
    financial_metrics = {
        "P/E Ratio": info.get("trailingPE", "N/A"),
        "P/B Ratio": info.get("priceToBook", "N/A"),
        "EPS": info.get("trailingEps", "N/A"),
        "Dividend Yield": info.get("dividendYield", "N/A"),
        "Profit Margin": info.get("profitMargins", "N/A"),
        "ROE": info.get("returnOnEquity", "N/A"),
    }

    st.subheader("Financial Metrics")
    metric_df = pd.DataFrame(list(financial_metrics.items()), columns=["Metric", "Value"])
    st.table(metric_df)

# Display stock price chart
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
        yaxis_title="Price (USD)"
    )
    st.plotly_chart(fig)

# Investment recommendation
def display_recommendation(info):
    pe_ratio = info.get("trailingPE")
    if pe_ratio:
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
        stock_data = fetch_stock_data(ticker)

        if stock_data:
            info = stock_data["info"]
            history = stock_data["history"]

            display_company_profile(info)
            display_financial_metrics(info)
            display_recommendation(info)
            display_stock_chart(history, ticker)
        else:
            st.error("Failed to fetch data. Please check the ticker symbol and try again.")

if __name__ == "__main__":
    main()
