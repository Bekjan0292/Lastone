import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd

# Page Config
st.set_page_config(page_title="Stock Fundamental Analysis", layout="wide")

# Sidebar
st.sidebar.title("Stock Analysis")
ticker = st.sidebar.text_input("Enter Stock Ticker:", value="AAPL")

# Fetch Data for Main Section
if ticker:
    stock = yf.Ticker(ticker)
    info = stock.info
    historical = stock.history(period="1y")
    
    # Layout
    st.title(f"{info['longName']} ({ticker.upper()})")
    
    # About the Company - Expandable Section
    with st.expander("About the Company"):
        if "longBusinessSummary" in info:
            st.write(info['longBusinessSummary'])
        else:
            st.write("Company information is not available.")
    
    # Display Industry, Country, and Website
    st.write(f"**Industry:** {info.get('industry', 'N/A')}")
    st.write(f"**Country:** {info.get('country', 'N/A')}")
    if "website" in info:
        st.markdown(f"[**Website**]({info['website']})", unsafe_allow_html=True)
    else:
        st.write("**Website:** N/A")
    
    # Japanese Candlestick Chart
    fig = go.Figure()
    fig.add_trace(
        go.Candlestick(
            x=historical.index,
            open=historical['Open'],
            high=historical['High'],
            low=historical['Low'],
            close=historical['Close'],
            name='Candlesticks'
        )
    )
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        template="plotly_white",
        hovermode="x",
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Key statistics in compact table format
    st.subheader("Key Statistics")
    stats_data = [
        [f"*Current Price*", f"${info['currentPrice']:.2f}", f"*Market Cap*", f"${info['marketCap'] / 1e9:.2f}B"],
        [f"*52W Range*", f"{info['fiftyTwoWeekLow']} - {info['fiftyTwoWeekHigh']}", f"*Previous Close*", f"${info['previousClose']}"],
        [f"*Open*", f"${info['open']}", f"*Day's Range*", f"{info['dayLow']} - {info['dayHigh']}"],
        [f"*Beta*", f"{info['beta']}", f"*Forward PE*", f"{info.get('forwardPE', 'N/A')}"],
        [f"*Dividend Yield*", f"{info.get('dividendYield', 0) * 100:.2f}%", "", ""]
    ]
    
    # Create a DataFrame without headers
    stats_df = pd.DataFrame(stats_data)
    st.table(stats_df.style.hide(axis='columns'))
    
    # Financial metrics
    st.subheader("Financial Analysis")
    with st.expander("Income Statement"):
        st.write("Revenue, Net Income, etc.")
    with st.expander("Balance Sheet"):
        st.write("Total Assets, Liabilities, etc.")
    with st.expander("Cash Flow"):
        st.write("Operating Cash Flow, etc.")
else:
    st.warning("Please enter a valid ticker symbol.")
