import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objs as go

# Streamlit page settings
st.set_page_config(page_title="Stock Analysis Dashboard", layout="wide", initial_sidebar_state="expanded")

# Helper functions
@st.cache_data
def load_stock_data(ticker, start_date, end_date):
    stock = yf.Ticker(ticker)
    return stock.history(start=start_date, end=end_date)

@st.cache_data
def get_company_info(ticker):
    stock = yf.Ticker(ticker)
    return {
        "Sector": stock.info.get("sector", "N/A"),
        "Country": stock.info.get("country", "N/A"),
        "PE Ratio": stock.info.get("trailingPE", "N/A"),
        "PB Ratio": stock.info.get("priceToBook", "N/A"),
        "EPS": stock.info.get("trailingEps", "N/A"),
        "Revenue": stock.info.get("totalRevenue", "N/A"),
        "Net Income": stock.info.get("netIncomeToCommon", "N/A"),
        "Debt to Equity": stock.info.get("debtToEquity", "N/A"),
        "Dividend Yield": stock.info.get("dividendYield", "N/A"),
    }

# Technical Indicators
def calculate_sma(data, period=50):
    return data['Close'].rolling(window=period).mean()

def calculate_rsi(data, period=20):
    delta = data['Close'].diff(1)
    gain = delta.where(delta > 0, 0).rolling(window=period).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def calculate_macd(data):
    ema_12 = data['Close'].ewm(span=12, adjust=False).mean()
    ema_26 = data['Close'].ewm(span=26, adjust=False).mean()
    return ema_12 - ema_26

# Main app
def main():
    st.sidebar.header("Options")
    ticker = st.sidebar.text_input("Stock symbol:", "AAPL")
    start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2021-01-01"))
    end_date = st.sidebar.date_input("End Date", pd.to_datetime("today"))
    
    # Analysis selection
    analysis_type = st.sidebar.selectbox("Select Analysis Type:", ["Fundamental Analysis", "Technical Analysis"])
    
    # Load data
    stock_data = load_stock_data(ticker, start_date, end_date)
    company_info = get_company_info(ticker)

    if analysis_type == "Fundamental Analysis":
        st.header("Fundamental Analysis")
        
        # Display basic company info
        st.write("### Company Information")
        st.write(f"**Sector:** {company_info['Sector']}")
        st.write(f"**Country:** {company_info['Country']}")
        
        # Display additional financial metrics
        st.write("### Financial Metrics")
        st.write(f"**P/E Ratio:** {company_info['PE Ratio']}")
        st.write(f"**P/B Ratio:** {company_info['PB Ratio']}")
        st.write(f"**EPS:** {company_info['EPS']}")
        st.write(f"**Revenue:** {company_info['Revenue']:,}" if company_info['Revenue'] != "N/A" else "**Revenue:** N/A")
        st.write(f"**Net Income:** {company_info['Net Income']:,}" if company_info['Net Income'] != "N/A" else "**Net Income:** N/A")
        st.write(f"**Debt to Equity Ratio:** {company_info['Debt to Equity']}")
        st.write(f"**Dividend Yield:** {company_info['Dividend Yield']}")
        
        # Recommendations
        st.write("### Recommendation")
        if company_info['PE Ratio'] != "N/A" and company_info['PE Ratio'] < 15:
            st.write("**Recommendation:** Buy (Undervalued)")
        elif company_info['PE Ratio'] != "N/A" and company_info['PE Ratio'] > 25:
            st.write("**Recommendation:** Sell (Overvalued)")
        else:
            st.write("**Recommendation:** Hold (Fairly Valued)")
    
    elif analysis_type == "Technical Analysis":
        st.header("Technical Analysis")
        
        # Calculate indicators
        short_ma_days = st.sidebar.slider("Short-term moving average days:", 10, 100, 10)
        long_ma_days = st.sidebar.slider("Long-term moving average days:", 50, 200, 50)
        stock_data['SMA_Short'] = calculate_sma(stock_data, short_ma_days)
        stock_data['SMA_Long'] = calculate_sma(stock_data, long_ma_days)
        stock_data['RSI'] = calculate_rsi(stock_data, 20)
        stock_data['MACD'] = calculate_macd(stock_data)
        
        # Plot charts
        st.write("### Price and Moving Averages")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['Close'], mode='lines', name="Close Price"))
        fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['SMA_Short'], mode='lines', name=f"SMA {short_ma_days}"))
        fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['SMA_Long'], mode='lines', name=f"SMA {long_ma_days}"))
        fig.update_layout(template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
        
        st.write("### RSI (20)")
        fig_rsi = go.Figure()
        fig_rsi.add_trace(go.Scatter(x=stock_data.index, y=stock_data['RSI'], mode='lines', name="RSI"))
        fig_rsi.update_layout(template="plotly_dark")
        st.plotly_chart(fig_rsi, use_container_width=True)
        
        st.write("### MACD")
        fig_macd = go.Figure()
        fig_macd.add_trace(go.Scatter(x=stock_data.index, y=stock_data['MACD'], mode='lines', name="MACD"))
        fig_macd.update_layout(template="plotly_dark")
        st.plotly_chart(fig_macd, use_container_width=True)

if __name__ == "__main__":
    main()
