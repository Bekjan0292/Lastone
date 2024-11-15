import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import talib

# Streamlit page settings
st.set_page_config(page_title="Enhanced Stock Analysis Dashboard", layout="wide", initial_sidebar_state="expanded")

# Helper functions
@st.cache_data
def load_stock_data(ticker, start_date, end_date):
    stock = yf.Ticker(ticker)
    return stock.history(start=start_date, end=end_date)

@st.cache_data
def get_company_info(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    return {
        "Company Name": info.get("shortName", "N/A"),
        "Sector": info.get("sector", "N/A"),
        "Industry": info.get("industry", "N/A"),
        "Country": info.get("country", "N/A"),
        "PE Ratio": info.get("trailingPE", "N/A"),
        "PB Ratio": info.get("priceToBook", "N/A"),
        "EPS": info.get("trailingEps", "N/A"),
        "Revenue": info.get("totalRevenue", "N/A"),
        "Net Income": info.get("netIncomeToCommon", "N/A"),
        "Debt to Equity": info.get("debtToEquity", "N/A"),
        "Dividend Yield": info.get("dividendYield", "N/A"),
        "Profit Margin": info.get("profitMargins", "N/A"),
        "Current Ratio": info.get("currentRatio", "N/A"),
        "Quick Ratio": info.get("quickRatio", "N/A"),
        "ROE": info.get("returnOnEquity", "N/A"),
        "Market Cap": info.get("marketCap", "N/A"),
    }

# Technical Indicators
def calculate_bollinger_bands(data, period=20, std_dev=2):
    upper_band, middle_band, lower_band = talib.BBANDS(data['Close'], timeperiod=period, nbdevup=std_dev, nbdevdn=std_dev)
    return upper_band, middle_band, lower_band

def calculate_stochastic_oscillator(data, period=14):
    k, d = talib.STOCH(data['High'], data['Low'], data['Close'], fastk_period=period, slowk_period=3, slowd_period=3)
    return k, d

# Moving Averages
def calculate_sma(data, period):
    return talib.SMA(data['Close'], timeperiod=period)

def calculate_rsi(data, period):
    return talib.RSI(data['Close'], timeperiod=period)

def calculate_macd(data):
    macd, signal, hist = talib.MACD(data['Close'], fastperiod=12, slowperiod=26, signalperiod=9)
    return macd, signal, hist

# Main app
def main():
    st.sidebar.header("Options")
    ticker = st.sidebar.text_input("Stock symbol:", "AAPL", key="ticker_input")
    start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2021-01-01"), key="start_date_input")
    end_date = st.sidebar.date_input("End Date", pd.to_datetime("today"), key="end_date_input")

    # Analysis selection
    analysis_type = st.sidebar.selectbox("Select Analysis Type:", ["Fundamental Analysis", "Technical Analysis"], key="analysis_selectbox")

    # Load data
    stock_data = load_stock_data(ticker, start_date, end_date)
    company_info = get_company_info(ticker)

    if analysis_type == "Fundamental Analysis":
        st.header("Fundamental Analysis")

        # Display basic company info
        st.write("### Company Overview")
        st.write(f"**Company Name:** {company_info['Company Name']}")
        st.write(f"**Sector:** {company_info['Sector']}")
        st.write(f"**Industry:** {company_info['Industry']}")
        st.write(f"**Country:** {company_info['Country']}")

        # Display financial metrics with explanations
        st.write("### Key Financial Metrics")

        # P/E Ratio (Price-to-Earnings)
        st.write(f"**P/E Ratio (Price-to-Earnings):** {company_info['PE Ratio']}")
        st.write("A higher P/E ratio suggests that investors are willing to pay more for a company's earnings, often indicating high expectations for future growth.")

        # P/B Ratio (Price-to-Book)
        st.write(f"**P/B Ratio (Price-to-Book):** {company_info['PB Ratio']}")
        st.write("The P/B ratio compares a company's market value to its book value. A ratio above 1 means the stock is trading for more than its book value, suggesting strong growth expectations.")

        # EPS (Earnings Per Share)
        st.write(f"**EPS (Earnings Per Share):** {company_info['EPS']}")
        st.write("EPS indicates the profitability of a company. A higher EPS typically reflects better financial performance.")

        # Revenue
        st.write(f"**Revenue:** {company_info['Revenue']:,}" if company_info['Revenue'] != 'N/A' else "**Revenue:** N/A")
        st.write("Revenue is the total amount of money the company brings in. It's often used to assess the size and growth potential of a business.")

        # Net Income
        st.write(f"**Net Income:** {company_info['Net Income']:,}" if company_info['Net Income'] != 'N/A' else "**Net Income:** N/A")
        st.write("Net Income is the profit of a company after all expenses are subtracted. It's a key indicator of financial health.")

        # Debt to Equity Ratio
        st.write(f"**Debt to Equity Ratio:** {company_info['Debt to Equity']}")
        st.write("A lower Debt-to-Equity ratio indicates lower financial risk. A ratio higher than 1 means the company has more debt than equity.")

        # Dividend Yield
        st.write(f"**Dividend Yield:** {company_info['Dividend Yield']}")
        st.write("Dividend yield represents the annual return on investment from dividends. A high dividend yield might appeal to income investors.")

        # Profit Margin
        st.write(f"**Profit Margin:** {company_info['Profit Margin']}")
        st.write("Profit margin is the percentage of revenue that turns into profit. A higher profit margin indicates better profitability.")

        # Current Ratio
        st.write(f"**Current Ratio:** {company_info['Current Ratio']}")
        st.write("The current ratio measures a company's ability to pay off its short-term liabilities with its short-term assets. A ratio greater than 1 is considered healthy.")

        # Quick Ratio
        st.write(f"**Quick Ratio:** {company_info['Quick Ratio']}")
        st.write("The quick ratio is similar to the current ratio but excludes inventory. It provides a stricter measure of liquidity.")

        # ROE (Return on Equity)
        st.write(f"**ROE (Return on Equity):** {company_info['ROE']}")
        st.write("ROE measures a company's profitability by comparing net income to shareholders' equity. A higher ROE suggests efficient management.")

        # Market Cap
        st.write(f"**Market Cap:** {company_info['Market Cap']}")
        st.write("Market capitalization reflects the total value of a company's outstanding shares. It's used to classify companies into categories like large-cap, mid-cap, or small-cap.")

        st.write("### Additional Insights")
        st.write("These metrics collectively give investors an understanding of the company's financial health, growth prospects, and risk levels. A well-rounded analysis of these metrics helps to assess the stock's potential in the market.")

    elif analysis_type == "Technical Analysis":
        st.header("Technical Analysis")

        # Calculate indicators
        short_ma_days = st.sidebar.slider("Short-term moving average days:", 10, 100, 10)
        long_ma_days = st.sidebar.slider("Long-term moving average days:", 50, 200, 50)
        stock_data['SMA_Short'] = calculate_sma(stock_data, short_ma_days)
        stock_data['SMA_Long'] = calculate_sma(stock_data, long_ma_days)
        stock_data['RSI'] = calculate_rsi(stock_data, 20)
        stock_data['MACD'], stock_data['MACD Signal'], stock_data['MACD Hist'] = calculate_macd(stock_data)
        stock_data['UpperBB'], stock_data['MiddleBB'], stock_data['LowerBB'] = calculate_bollinger_bands(stock_data)
        stock_data['K'], stock_data['D'] = calculate_stochastic_oscillator(stock_data)

        # Plot charts
        st.write("### Price and Moving Averages")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['Close'], mode='lines', name="Price"))
        fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['SMA_Short'], mode='lines', name=f"SMA ({short_ma_days} days)"))
        fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['SMA_Long'],
