
import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd

# Page Config
st.set_page_config(page_title="Stock Fundamental Analysis", layout="wide")

# Main Input Section
st.title("Stock Fundamental Analysis")
ticker = st.text_input("Enter Stock Ticker:", value="AAPL")
go_button = st.button("Go")

# Fetch Data when "Go" is clicked
if go_button and ticker:
    stock = yf.Ticker(ticker)
    info = stock.info
    historical = stock.history(period="1y")
    
    # Display Stock Information
    st.title(f"{info['longName']} ({ticker.upper()})")
    
    # About the Company - Expandable Section
    with st.expander("About the Company"):
        if "longBusinessSummary" in info:
            st.write(info["longBusinessSummary"])
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
        yaxis_title="Price",
        title="1-Year Stock Price Candlestick Chart"
    )
    st.plotly_chart(fig)
