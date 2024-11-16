import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

st.title("Technical Analysis")

if "ticker" not in st.session_state or not st.session_state["ticker"]:
    st.warning("Please enter a stock ticker on the 'Enter Ticker' page first.")
else:
    ticker = st.session_state["ticker"]

    stock = yf.Ticker(ticker)
    history = stock.history(period="1y")

    st.subheader("Price Chart (Last 1 Year)")
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=history.index,
        open=history['Open'],
        high=history['High'],
        low=history['Low'],
        close=history['Close'],
        name="Price"
    ))
    fig.update_layout(
        title="Price Chart",
        xaxis_title="Date",
        yaxis_title="Price",
        xaxis_rangeslider_visible=False
    )
    st.plotly_chart(fig)

    st.subheader("Moving Averages")
    history['SMA_50'] = history['Close'].rolling(window=50).mean()
    history['SMA_200'] = history['Close'].rolling(window=200).mean()
    st.line_chart(history[['Close', 'SMA_50', 'SMA_200']])
