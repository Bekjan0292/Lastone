import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

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
        data = stock.history(period="1y")
        if not data.empty:
            portfolio_data[ticker] = data
        else:
            st.sidebar.warning(f"No data for {ticker}.")
    except Exception as e:
        st.sidebar.warning(f"Error retrieving data for {ticker}: {e}")

# Portfolio Overview
st.header("Portfolio Overview")

if portfolio_data:
    col1, col2, col3 = st.columns(3)
    with col1:
        total_value = sum([df["Close"].iloc[-1] for df in portfolio_data.values()])
        st.metric("Total Value", f"${total_value:,.2f}")

    with col2:
        total_returns = sum([(df["Close"].iloc[-1] - df["Close"].iloc[0]) / df["Close"].iloc[0] * 100
                             for df in portfolio_data.values() if len(df) > 1])
        st.metric("Total Returns", f"{total_returns / len(portfolio_data):.2f}%")

    with col3:
        avg_dividend_yield = sum([yf.Ticker(ticker).info.get("dividendYield", 0) 
                                  for ticker in portfolio_data.keys()]) / len(portfolio_data)
        avg_dividend_yield = avg_dividend_yield if avg_dividend_yield else 0
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
    categories = ["Dividend", "Value", "Future", "Health", "Past"]
    sample_values = [3, 4, 2, 5, 3]  # Replace with actual calculations if possible
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
        st.metric("Total Expected Dividends", f"${avg_dividend_yield * total_value:.2f}")

    with col2:
        st.metric("Yield on Cost", f"{avg_dividend_yield * 100:.2f}%")

    # Management and Key Information
    st.subheader("Management & Key Information")
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        st.write(f"### {ticker} - {stock.info.get('longName', 'Company Name Not Available')}")
        st.write(f"CEO: {stock.info.get('ceo', 'N/A')}")
        st.write(f"Market Cap: {stock.info.get('marketCap', 'Data Not Available')}")
        st.write("---")
else:
    st.warning("No valid portfolio data available.")
