import streamlit as st
import yfinance as yf

# Page Config
st.set_page_config(page_title="Stock Fundamental Analysis", layout="wide")

# Sidebar
st.sidebar.title("Stock Analysis")
ticker = st.sidebar.text_input("Enter Stock Ticker:", value="AAPL")

# Fetch Data
if ticker:
    stock = yf.Ticker(ticker)
    info = stock.info
    
    # Layout
    st.title(f"{info['longName']} ({ticker.upper()})")
    
    # Price and summary section
    st.write(
        f"**Current Price:** ${info['currentPrice']:.2f}  "
        f"**Market Cap:** ${info['marketCap'] / 1e9:.2f}B  "
        f"**52W Range:** {info['fiftyTwoWeekLow']} - {info['fiftyTwoWeekHigh']}"
    )
    
    # Line chart
    st.line_chart(stock.history(period="1y")['Close'])
    
    # Key statistics
    st.subheader("Key Statistics")
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Previous Close:** {info['previousClose']}")
        st.write(f"**Open:** {info['open']}")
        st.write(f"**Day's Range:** {info['dayLow']} - {info['dayHigh']}")
    with col2:
        st.write(f"**Beta:** {info['beta']}")
        st.write(f"**Forward PE:** {info.get('forwardPE', 'N/A')}")
        st.write(f"**Dividend Yield:** {info.get('dividendYield', 'N/A') * 100:.2f}%")
    
    # Financial metrics
    st.subheader("Financial Analysis")
    st.write("Income Statement, Balance Sheet, and Cash Flow data can be displayed here.")
else:
    st.warning("Please enter a valid ticker symbol.")
