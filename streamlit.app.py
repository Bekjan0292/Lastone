import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import ta

# Title and Description
st.title("Investment Analysis Dashboard: Fundamental and Technical Analysis")
st.markdown("""
This app provides both **Fundamental** and **Technical Analysis** for stocks. 
It fetches stock data, calculates key financial ratios, and visualizes price trends and indicators.
""")

# User Input: Stock Ticker
ticker = st.text_input("Enter Stock Ticker (e.g., AAPL, MSFT):", value="AAPL")

# Fetch Stock Data
if ticker:
    stock = yf.Ticker(ticker)
    info = stock.info
    financials = stock.financials
    history = stock.history(period="1y")
    
    # ---- Fundamental Analysis ----
    st.header(f"Fundamental Analysis of {ticker}")
    
    # Market Cap in millions
    market_cap = info['marketCap'] / 1_000_000
    st.metric("Market Cap (in millions)", f"${market_cap:,.0f}M")
    
    # Key Financial Ratios
    ratios = {
        "P/E Ratio": info.get("trailingPE", 'N/A'),
        "Price/Book": info.get("priceToBook", 'N/A'),
        "Return on Equity (ROE)": info.get("returnOnEquity", 'N/A'),
        "Dividend Yield": info.get("dividendYield", 'N/A') * 100
    }
    st.write(pd.DataFrame(ratios.items(), columns=["Ratio", "Value"]))
    
    # Financial Statement Trends (Revenue and Net Income)
    st.subheader("Financial Trends")
    fig, ax = plt.subplots()
    financials.loc['Total Revenue'].plot(kind='line', label='Revenue', ax=ax)
    financials.loc['Net Income'].plot(kind='line', label='Net Income', ax=ax)
    ax.set_title("Revenue vs. Net Income")
    ax.legend()
    st.pyplot(fig)

    # ---- Technical Analysis ----
    st.header(f"Technical Analysis of {ticker}")
    
    # Plot stock price chart with moving averages
    st.subheader("Price Chart with Moving Averages")
    history['SMA50'] = history['Close'].rolling(window=50).mean()
    history['SMA200'] = history['Close'].rolling(window=200).mean()
    
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=history.index,
        open=history['Open'],
        high=history['High'],
        low=history['Low'],
        close=history['Close'],
        name='Candlesticks'
    ))
    fig.add_trace(go.Scatter(
        x=history.index, y=history['SMA50'], mode='lines', name='50-day SMA'
    ))
    fig.add_trace(go.Scatter(
        x=history.index, y=history['SMA200'], mode='lines', name='200-day SMA'
    ))
    st.plotly_chart(fig)

    # Add technical indicators (RSI and MACD)
    st.subheader("RSI and MACD")
    
    # Calculate RSI using ta library
    history['RSI'] = ta.momentum.RSIIndicator(history['Close'], window=14).rsi()
    
    # Calculate MACD using ta library
    macd = ta.trend.MACD(history['Close'])
    history['MACD'] = macd.macd()
    history['MACD_signal'] = macd.macd_signal()
    
    fig, ax = plt.subplots(2, 1, figsize=(10, 8))
    
    # Plot RSI
    ax[0].plot(history.index, history['RSI'], label='RSI')
    ax[0].axhline(70, color='r', linestyle='--', label='Overbought')
    ax[0].axhline(30, color='g', linestyle='--', label='Oversold')
    ax[0].set_title("RSI (Relative Strength Index)")
    ax[0].legend()
    
    # Plot MACD
    ax[1].plot(history.index, history['MACD'], label='MACD')
    ax[1].plot(history.index, history['MACD_signal'], label='MACD Signal', linestyle='--')
    ax[1].set_title("MACD (Moving Average Convergence Divergence)")
    ax[1].legend()

    st.pyplot(fig)
    
else:
    st.info("Please enter a stock ticker to begin analysis.")
