import streamlit as st
import yfinance as yf
import pandas as pd
from streamlit_echarts import st_echarts
from st_aggrid import AgGrid, GridOptionsBuilder
import plotly.graph_objs as go

# Streamlit page settings
st.set_page_config(
    page_title="Stock Analysis Dashboard",
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

# Display fundamental analysis using streamlit-echarts for a radar chart
def display_fundamental_analysis(info):
    st.header("Company Overview")
    
    # Display Company Details
    st.subheader(info.get("shortName", "N/A"))
    st.write(info.get("longBusinessSummary", "N/A"))
    
    # Radar chart for financial metrics comparison
    financial_data = {
        "P/E Ratio": info.get("trailingPE", 0),
        "P/B Ratio": info.get("priceToBook", 0),
        "EPS": info.get("trailingEps", 0),
        "Dividend Yield": info.get("dividendYield", 0),
        "Profit Margin": info.get("profitMargins", 0),
        "ROE": info.get("returnOnEquity", 0),
    }

    radar_option = {
        "title": {"text": "Financial Metrics Comparison"},
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
            "name": "Financial Metrics",
            "type": "radar",
            "data": [{"value": list(financial_data.values()), "name": "Metrics"}]
        }]
    }

    st_echarts(radar_option, height="400px")

# Display financial metrics in a styled, interactive table using st_aggrid
def display_financial_metrics(info):
    st.subheader("Key Financial Metrics")

    # Interactive table with AgGrid
    financial_metrics = {
        "Metric": ["P/E Ratio", "P/B Ratio", "EPS", "Dividend Yield", "Profit Margin", "ROE"],
        "Value": [
            info.get("trailingPE", "N/A"),
            info.get("priceToBook", "N/A"),
            info.get("trailingEps", "N/A"),
            info.get("dividendYield", "N/A"),
            info.get("profitMargins", "N/A"),
            info.get("returnOnEquity", "N/A")
        ]
    }

    metrics_df = pd.DataFrame(financial_metrics)
    
    # Configure AgGrid options for interactive experience
    gb = GridOptionsBuilder.from_dataframe(metrics_df)
    gb.configure_pagination(paginationAutoPageSize=True)
    gb.configure_side_bar()  # Enable sidebar for filtering
    gridOptions = gb.build()

    AgGrid(metrics_df, gridOptions=gridOptions, theme='light')

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
    st.title("Stock Analysis Dashboard")

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
