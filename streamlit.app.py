import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd

# App title
st.title("Stock Analyzer App")
st.sidebar.header("Stock Selection")

# Stock selection input
ticker = st.sidebar.text_input("Enter stock ticker (e.g., AAPL, TSLA):", value="AAPL").upper()

if ticker:
    # Fetch stock data
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        history = stock.history(period="1y")  # Last 1 year of data

        # Display fundamental information
        st.header(f"{info.get('longName', 'Unknown Company')} ({info.get('symbol', ticker)})")
        st.subheader("Fundamental Analysis")
        st.markdown(f"""
        **Sector**: {info.get('sector', 'N/A')}  
        **Industry**: {info.get('industry', 'N/A')}  
        **Market Cap**: ${info.get('marketCap', 0):,}  
        **PE Ratio (TTM)**: {info.get('forwardPE', 'N/A')}  
        **Dividend Yield**: {info.get('dividendYield', 0) * 100:.2f}%  
        **52-Week High**: ${info.get('fiftyTwoWeekHigh', 'N/A')}  
        **52-Week Low**: ${info.get('fiftyTwoWeekLow', 'N/A')}  
        """)

        # Display stock price chart
        st.subheader("Technical Analysis")
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
            title="Price Chart (Last 1 Year)",
            xaxis_title="Date",
            yaxis_title="Price",
            xaxis_rangeslider_visible=False
        )
        st.plotly_chart(fig)

        # Moving averages
        st.markdown("**Moving Averages**")
        history['SMA_50'] = history['Close'].rolling(window=50).mean()
        history['SMA_200'] = history['Close'].rolling(window=200).mean()
        st.line_chart(history[['Close', 'SMA_50', 'SMA_200']])

    except Exception as e:
        st.error(f"Error fetching data for {ticker}. Details: {e}")

else:
    st.info("Please enter a valid stock ticker to start analysis.")
