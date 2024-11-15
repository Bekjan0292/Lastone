import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go

# Streamlit page settings
st.set_page_config(
    page_title="Stock Analysis Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Simply Wall St-like design
st.markdown("""
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f5f7fa;
            color: #333;
        }
        .card {
            border-radius: 8px;
            padding: 20px;
            margin: 10px;
            background-color: #ffffff;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
        }
        .card h3 {
            color: #0073e6;
        }
        .metric-container {
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
        }
        .metric-container .metric {
            flex: 1;
            min-width: 180px;
            text-align: center;
            padding: 15px;
            border-radius: 8px;
            background-color: #f0f2f5;
            box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
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

# Display fundamental analysis
def display_fundamental_analysis(info):
    st.header("Company Overview")

    # Create card layout for fundamental data
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader(info.get("shortName", "N/A"))
    st.write(info.get("longBusinessSummary", "N/A"))
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
    st.markdown("<div class='metric'><h3>Sector</h3><p>{}</p></div>".format(info.get("sector", "N/A")), unsafe_allow_html=True)
    st.markdown("<div class='metric'><h3>Industry</h3><p>{}</p></div>".format(info.get("industry", "N/A")), unsafe_allow_html=True)
    st.markdown("<div class='metric'><h3>Website</h3><p><a href='{}' target='_blank'>{}</a></p></div>".format(info.get("website", "#"), info.get("website", "N/A")), unsafe_allow_html=True)
    st.markdown("<div class='metric'><h3>Market Cap</h3><p>${:,}</p></div>".format(info.get("marketCap", "N/A")) if info.get("marketCap") else "<p>N/A</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Display financial metrics in a styled table
def display_financial_metrics(info):
    st.subheader("Key Financial Metrics")
    
    # Display financial metrics in a table format with additional styling
    financial_metrics = {
        "P/E Ratio": info.get("trailingPE", "N/A"),
        "P/B Ratio": info.get("priceToBook", "N/A"),
        "EPS": info.get("trailingEps", "N/A"),
        "Dividend Yield": info.get("dividendYield", "N/A"),
        "Profit Margin": info.get("profitMargins", "N/A"),
        "ROE": info.get("returnOnEquity", "N/A"),
    }

    metric_df = pd.DataFrame(list(financial_metrics.items()), columns=["Metric", "Value"])
    st.table(metric_df)

# Display interactive stock price chart
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
