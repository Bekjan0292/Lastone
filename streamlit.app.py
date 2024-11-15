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

# Display fundamental analysis (similar to attached screenshot)
def display_fundamental_analysis(info):
    st.header("Fundamental Analysis")
    
    st.metric("Sector", info.get("sector", "N/A"))
    st.metric("Industry", info.get("industry", "N/A"))
    st.metric("Website", info.get("website", "N/A"))
    st.metric("Market Cap", f"${info.get('marketCap', 'N/A'):,}" if info.get("marketCap") else "N/A")

    with st.expander("About Company"):
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

# Display interactive stock price chart
def display_stock_chart(history, ticker):
    st.subheader("Interactive Stock Price Chart")
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
    st.title("Interactive Stock Analysis")

    if fetch_data:
        st.subheader(f"Analyzing {ticker.upper()} Data")
        stock_data = fetch_stock_data(ticker)

        if stock_data:
            info = stock_data["info"]
            history = stock_data["history"]

            display_fundamental_analysis(info)
            display_financial_metrics(info)
            display_stock_chart(history, ticker)
        else:
            st.error("Failed to fetch data. Please check the ticker symbol and try again.")

if __name__ == "__main__":
    main()
