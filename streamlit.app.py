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
    st.write(stock.info)  # Debug: Print full info dictionary for troubleshooting
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
        "Profit Margin": stock.info.get("profitMargins", "N/A"),
        "Current Ratio": stock.info.get("currentRatio", "N/A"),
        "Quick Ratio": stock.info.get("quickRatio", "N/A"),
        "ROE": stock.info.get("returnOnEquity", "N/A"),
    }

# Technical Indicators
def calculate_bollinger_bands(data, period=20, std_dev=2):
    upper_band, middle_band, lower_band = talib.BBANDS(data['Close'].values, timeperiod=period, nbdevup=std_dev, nbdevdn=std_dev)
    return upper_band, middle_band, lower_band

def calculate_stochastic_oscillator(data, period=14):
    k, d = talib.STOCH(data['High'].values, data['Low'].values, data['Close'].values, fastk_period=period, slowk_period=3, slowd_period=3)
    return k, d

def calculate_sma(data, period=50):
    return data['Close'].rolling(window=period).mean()

def calculate_rsi(data, period=14):
    delta = data['Close'].diff()
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)
    avg_gain = pd.Series(gain).rolling(window=period).mean()
    avg_loss = pd.Series(loss).rolling(window=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_macd(data):
    ema12 = data['Close'].ewm(span=12, adjust=False).mean()
    ema26 = data['Close'].ewm(span=26, adjust=False).mean()
    macd = ema12 - ema26
    return macd

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
        st.write("### Company Information")
        st.write(f"**Sector:** {company_info['Sector']}")
        st.write(f"**Country:** {company_info['Country']}")

        st.write("### Financial Metrics")
        metrics = {
            "P/E Ratio": company_info['PE Ratio'],
            "P/B Ratio": company_info['PB Ratio'],
            "EPS": company_info['EPS'],
            "Revenue": company_info['Revenue'],
            "Net Income": company_info['Net Income'],
            "Debt to Equity Ratio": company_info['Debt to Equity'],
            "Dividend Yield": company_info['Dividend Yield'],
            "Profit Margin": company_info['Profit Margin'],
            "Current Ratio": company_info['Current Ratio'],
            "Quick Ratio": company_info['Quick Ratio'],
            "ROE": company_info['ROE'],
        }
        for key, value in metrics.items():
            st.write(f"**{key}:** {value if value != 'N/A' else 'Data not available'}")

    elif analysis_type == "Technical Analysis":
        st.header("Technical Analysis")
        short_ma_days = st.sidebar.slider("Short-term moving average days:", 10, 100, 10)
        long_ma_days = st.sidebar.slider("Long-term moving average days:", 50, 200, 50)

        stock_data['SMA_Short'] = calculate_sma(stock_data, short_ma_days)
        stock_data['SMA_Long'] = calculate_sma(stock_data, long_ma_days)
        stock_data['RSI'] = calculate_rsi(stock_data)
        stock_data['MACD'] = calculate_macd(stock_data)
        stock_data['UpperBB'], stock_data['MiddleBB'], stock_data['LowerBB'] = calculate_bollinger_bands(stock_data)
        stock_data['K'], stock_data['D'] = calculate_stochastic_oscillator(stock_data)

        st.write("### Price and Moving Averages")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['Close'], name="Close Price"))
        fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['SMA_Short'], name=f"SMA {short_ma_days}"))
        fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['SMA_Long'], name=f"SMA {long_ma_days}"))
        fig.update_layout(title="Price with Moving Averages", template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

        st.write("### Bollinger Bands")
        fig_bb = go.Figure()
        fig_bb.add_trace(go.Scatter(x=stock_data.index, y=stock_data['Close'], name="Close Price"))
        fig_bb.add_trace(go.Scatter(x=stock_data.index, y=stock_data['UpperBB'], name="Upper Band"))
        fig_bb.add_trace(go.Scatter(x=stock_data.index, y=stock_data['LowerBB'], name="Lower Band"))
        fig_bb.update_layout(title="Bollinger Bands", template="plotly_dark")
        st.plotly_chart(fig_bb, use_container_width=True)

if __name__ == "__main__":
    main()
