import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# Title and Introduction
st.title("Stock Portfolio Dashboard")
st.markdown("""
This is an interactive portfolio analysis tool that allows you to view and analyze your stocks with key financial metrics.
You can also view price trends, moving averages, and get stock recommendations.
""")

# Display Logo (make sure you have a logo image in the folder)
st.image("logo.png", width=200)  # Make sure to add your logo.png in the same directory or specify the correct path

# User Input: Portfolio Ticker Upload or Example
uploaded_file = st.file_uploader("Upload your Portfolio CSV (with Tickers)", type=["csv"])

# Sample Portfolio if no file is uploaded
sample_portfolio = {
    "AAPL": "Apple Inc.",
    "MSFT": "Microsoft Corp.",
    "GOOGL": "Alphabet Inc.",
    "AMZN": "Amazon.com Inc.",
    "TSLA": "Tesla Inc."
}

# Default portfolio
if uploaded_file is not None:
    portfolio_df = pd.read_csv(uploaded_file)
else:
    st.markdown("**Sample Portfolio**")
    portfolio_df = pd.DataFrame({"Ticker": list(sample_portfolio.keys()), "Company": list(sample_portfolio.values())})

# Display Portfolio Table
st.write("### Portfolio Overview")
st.dataframe(portfolio_df)

# Fetch Stock Data and calculate financial metrics
def fetch_stock_data(ticker):
    stock = yf.Ticker(ticker)
    stock_data = stock.history(period="1y")
    return stock_data, stock.info

# Portfolio Analysis: Fetch data for each stock
for ticker in portfolio_df["Ticker"]:
    st.subheader(f"Stock: {ticker}")
    
    # Fetch data for stock and its info
    stock_data, stock_info = fetch_stock_data(ticker)

    # Stock Price Trend (last 1 year)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['Close'], mode='lines', name=f'{ticker} Closing Price'))
    fig.update_layout(title=f'{ticker} - Price Trend (Last 1 Year)', xaxis_title='Date', yaxis_title='Price (USD)')
    st.plotly_chart(fig)
    
    # Moving Averages: 50-day and 200-day
    stock_data['SMA50'] = stock_data['Close'].rolling(window=50).mean()
    stock_data['SMA200'] = stock_data['Close'].rolling(window=200).mean()
    
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=stock_data.index, y=stock_data['Close'], mode='lines', name='Stock Price'))
    fig2.add_trace(go.Scatter(x=stock_data.index, y=stock_data['SMA50'], mode='lines', name='50-Day Moving Average'))
    fig2.add_trace(go.Scatter(x=stock_data.index, y=stock_data['SMA200'], mode='lines', name='200-Day Moving Average'))
    fig2.update_layout(title=f'{ticker} - Moving Averages', xaxis_title='Date', yaxis_title='Price (USD)')
    st.plotly_chart(fig2)
    
    # Financial Metrics Table
    st.write("### Financial Metrics")
    financial_data = {
        "P/E Ratio": stock_info.get('trailingPE', 'N/A'),
        "P/B Ratio": stock_info.get('priceToBook', 'N/A'),
        "Return on Equity (ROE)": stock_info.get('returnOnEquity', 'N/A'),
        "Dividend Yield": f"{stock_info.get('dividendYield', 0) * 100}%",
        "Market Cap (M)": stock_info.get('marketCap', 'N/A') / 1_000_000
    }
    
    metrics_df = pd.DataFrame(list(financial_data.items()), columns=["Metric", "Value"])
    st.table(metrics_df)

    # Recommendation based on P/E ratio
    pe_ratio = stock_info.get('trailingPE', None)
    if pe_ratio:
        if pe_ratio < 15:
            st.markdown("**Recommendation**: Buy (Undervalued)")
        elif pe_ratio > 25:
            st.markdown("**Recommendation**: Sell (Overvalued)")
        else:
            st.markdown("**Recommendation**: Hold (Fairly Valued)")
    else:
        st.markdown("**Recommendation**: Data Unavailable")

# Portfolio Summary: Total Market Cap of Portfolio
st.header("Portfolio Summary")
total_market_cap = 0
for ticker in portfolio_df["Ticker"]:
    stock_info = yf.Ticker(ticker).info
    total_market_cap += stock_info.get('marketCap', 0)

st.markdown(f"**Total Market Cap of Portfolio**: ${total_market_cap / 1_000_000}M")

# Portfolio Performance Visualization: Combined Price Trend of all stocks
st.subheader("Portfolio Performance (Price Trend)")
fig3 = go.Figure()

for ticker in portfolio_df["Ticker"]:
    stock_data, _ = fetch_stock_data(ticker)
    fig3.add_trace(go.Scatter(x=stock_data.index, y=stock_data['Close'], mode='lines', name=ticker))

fig3.update_layout(title="Portfolio Price Trend (Last 1 Year)", xaxis_title="Date", yaxis_title="Price (USD)")
st.plotly_chart(fig3)

# Aggregated Portfolio Metrics: Example of average P/E ratio
pe_ratios = []
for ticker in portfolio_df["Ticker"]:
    stock_info = yf.Ticker(ticker).info
    pe_ratios.append(stock_info.get('trailingPE', 0))

average_pe = np.mean(pe_ratios)
st.write(f"**Average P/E Ratio of Portfolio**: {average_pe:.2f}")
