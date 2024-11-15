import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Page configuration
st.set_page_config(page_title="Portfolio Analysis Dashboard", layout="wide")

# App title
st.title("Portfolio Analysis Dashboard")

# Sidebar for input
ticker_list = st.sidebar.text_input("Enter ticker symbols separated by commas (e.g., AAPL, MSFT, TSLA)", value="AAPL, MSFT")
tickers = [ticker.strip() for ticker in ticker_list.split(",")]

# Data retrieval for portfolio
portfolio_data = {}
for ticker in tickers:
    try:
        stock = yf.Ticker(ticker)
        portfolio_data[ticker] = stock.history(period="1y")
    except Exception as e:
        st.sidebar.warning(f"Could not retrieve data for {ticker}")

# Portfolio Overview
st.header("Portfolio Overview")

# Performance Metrics
col1, col2, col3 = st.columns(3)
with col1:
    total_value = sum([df["Close"][-1] for df in portfolio_data.values()])
    st.metric("Total Value", f"${total_value:,.2f}")

with col2:
    total_returns = sum([(df["Close"][-1] - df["Close"][0]) / df["Close"][0] * 100 for df in portfolio_data.values()])
    st.metric("Total Returns", f"{total_returns / len(portfolio_data):.2f}%")

with col3:
    avg_dividend_yield = sum([stock.info.get("dividendYield", 0) for ticker, stock in portfolio_data.items()]) / len(portfolio_data)
    st.metric("Est. Dividend Yield", f"{avg_dividend_yield:.2f}%")

# Performance Chart
st.subheader("Performance vs Market")
fig, ax = plt.subplots(figsize=(10, 5))
for ticker, df in portfolio_data.items():
    ax.plot(df.index, df["Close"], label=ticker)
ax.set_title("Portfolio Performance Over Time")
ax.set_ylabel("Stock Price")
ax.legend()
st.pyplot(fig)

# Snowflake-style Financial Health
st.subheader("Portfolio Financial Health (Sample Representation)")

# Using a radar chart as an approximation for Snowflake Chart
import plotly.graph_objects as go

categories = ["Dividend", "Value", "Future", "Health", "Past"]
sample_values = [3, 4, 2, 5, 3]  # Example data, replace with actual calculations if possible

fig = go.Figure(data=go.Scatterpolar(
    r=sample_values,
    theta=categories,
    fill='toself'
))
fig.update_layout(polar=dict(
    radialaxis=dict(visible=True, range=[0, 5])
), showlegend=False)
st.plotly_chart(fig)

# Dividend Analysis
st.subheader("Dividend Analysis")
col1, col2 = st.columns(2)
with col1:
    st.write("**Next 12M Income**")
    st.metric("Total Expected Dividends", f"${avg_dividend_yield * total_value:.2f}")

with col2:
    st.write("**Dividend Yield on Cost**")
    yield_on_cost = avg_dividend_yield * 100
    st.metric("Yield on Cost", f"{yield_on_cost:.2f}%")

# Future Growth Forecasts (Sample Data)
st.subheader("Future Growth Forecasts")
forecast_data = pd.DataFrame({
    "Metric": ["Earnings Growth (next 3 years)", "Revenue Growth (next 3 years)", "Return on Equity (next 3 years)"],
    "Company": [5.2, 6.1, 8.4],
    "Industry": [4.5, 5.7, 7.8],
    "Market": [7.5, 6.9, 10.2]
})
fig = px.bar(forecast_data, x="Metric", y=["Company", "Industry", "Market"], barmode="group", title="Growth Forecasts Comparison")
st.plotly_chart(fig)

# Management and Key Information (Sample)
st.subheader("Management & Key Information")
for ticker in tickers:
    stock = yf.Ticker(ticker)
    st.write(f"### {ticker} - {stock.info.get('longName', 'Company Name Not Available')}")
    st.write(f"CEO: {stock.info.get('ceo', 'N/A')}")
    st.write(f"Market Cap: {stock.info.get('marketCap', 'N/A')}")
    st.write(f"Return on Equity: {stock.info.get('returnOnEquity', 'N/A')}")
    st.write("---")
