import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd

# Title
st.title("Stock Analyzer App")
st.sidebar.header("Stock Selection")

# Stock selection
ticker = st.sidebar.text_input("Enter stock ticker (e.g., AAPL, TSLA):", value="AAPL")

if ticker:
    # Fetch data
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        history = stock.history(period="1y")

        # Display fundamental information
        st.header(f"{info['shortName']} ({info['symbol']})")
        st.subheader("Fundamental Analysis")
        st.markdown(f"""
        **Sector**: {info['sector']}  
        **Industry**: {info['industry']}  
        **Market Cap**: ${info['marketCap']:,}  
        **PE Ratio (TTM)**: {info.get('forwardPE', 'N/A')}  
        **Dividend Yield**: {info.get('dividendYield', 'N/A') * 100:.2f}%  
        **52-Week High**: ${info['fiftyTwoWeekHigh']}  
        **52-Week Low**: ${info['fiftyTwoWeekLow']}  
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
            name='Candlestick'
        ))
        fig.update_layout(title="Price Chart (Last 1 Year)", xaxis_title="Date", yaxis_title="Price")
        st.plotly_chart(fig)

        # Indicators
        st.markdown("**Moving Averages**")
        history['SMA_50'] = history['Close'].rolling(window=50).mean()
        history['SMA_200'] = history['Close'].rolling(window=200).mean()
        st.line_chart(history[['Close', 'SMA_50', 'SMA_200']])

    except Exception as e:
        st.error(f"Error fetching data for {ticker}: {str(e)}")

else:
    st.info("Please enter a stock ticker to start analysis.")
