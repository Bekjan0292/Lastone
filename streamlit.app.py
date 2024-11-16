import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
import requests

# Page Config
st.set_page_config(page_title="Stock Fundamental Analysis", layout="wide")

# Sidebar
st.sidebar.title("Stock Analysis")
ticker = st.sidebar.text_input("Enter Stock Ticker:", value="AAPL")

# Additional ticker input for Profile functionality
ticker_input = st.text_input("Ticker for Profile Section", "NFLX").upper()
button_clicked = st.button("Set")

# Fetch Data for Main Section
if ticker:
    stock = yf.Ticker(ticker)
    info = stock.info
    historical = stock.history(period="1y")
    
    # Layout
    st.title(f"{info['longName']} ({ticker.upper()})")
    
    # Interactive Plotly chart
    st.subheader("Price History (1 Year)")
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=historical.index, 
            y=historical['Close'], 
            mode='lines',
            name='Close Price',
            line=dict(color='blue')
        )
    )
    fig.update_layout(
        title="Interactive Price Chart",
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        template="plotly_white",
        hovermode="x"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Key statistics in table format
    st.subheader("Key Statistics")
    stats_data = {
        "Metric": [
            "Current Price", 
            "Market Cap", 
            "52W Range", 
            "Previous Close", 
            "Open", 
            "Day's Range", 
            "Beta", 
            "Forward PE", 
            "Dividend Yield"
        ],
        "Value": [
            f"${info['currentPrice']:.2f}",
            f"${info['marketCap'] / 1e9:.2f}B",
            f"{info['fiftyTwoWeekLow']} - {info['fiftyTwoWeekHigh']}",
            f"${info['previousClose']}",
            f"${info['open']}",
            f"{info['dayLow']} - {info['dayHigh']}",
            f"{info['beta']}",
            f"{info.get('forwardPE', 'N/A')}",
            f"{info.get('dividendYield', 0) * 100:.2f}%"
        ]
    }
    stats_df = pd.DataFrame(stats_data)
    st.table(stats_df)
    
    # Financial metrics
    st.subheader("Financial Analysis")
    with st.expander("Income Statement"):
        st.write("Revenue, Net Income, etc.")
    with st.expander("Balance Sheet"):
        st.write("Total Assets, Liabilities, etc.")
    with st.expander("Cash Flow"):
        st.write("Operating Cash Flow, etc.")

# Fetch Data for Profile Section
if button_clicked:
    try:
        # Fetch data using Yahoo Finance API
        request_string = f"https://query1.finance.yahoo.com/v10/finance/quoteSummary/{ticker_input}?modules=assetProfile%2Cprice"
        request = requests.get(
            request_string, headers={"USER-AGENT": "Mozilla/5.0"}
        )
        json_data = request.json()
        data = json_data["quoteSummary"]["result"][0]

        # Display the "Profile" section
        st.header("Profile")
        st.metric("Sector", data["assetProfile"]["sector"])
        st.metric("Industry", data["assetProfile"]["industry"])
        st.metric("Website", data["assetProfile"]["website"])
        st.metric("Market Cap", data["price"]["marketCap"]["fmt"])

        with st.expander("About Company"):
            st.write(data["assetProfile"]["longBusinessSummary"])
    except Exception as e:
        st.error("Unable to fetch data. Please check the ticker or try again later.")
