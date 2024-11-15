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
    upper_band, middle_band, lower_band = talib.BBANDS(data['Close'], timeperiod=period, nbdevup=std_dev, nbdevdn=std_dev)
    return upper_band, middle_band, lower_band

def calculate_stochastic_oscillator(data, period=14):
    k, d = talib.STOCH(data['High'], data['Low'], data['Close'], fastk_period=period, slowk_period=3, slowd_period=3)
    return k, d

# Main app
def main():
    st.sidebar.header("Options")
    ticker = st.sidebar.text_input("Stock symbol:", "AAPL", key="ticker_input")
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

        # Display additional financial metrics with explanations
        st.write("### Key Financial Metrics")
        st.write(f"**P/E Ratio:** {company_info['PE Ratio']} - Price-to-Earnings ratio is used to value a company, comparing its current share price to its earnings per share. A lower P/E might indicate undervaluation.")
        st.write(f"**P/B Ratio:** {company_info['PB Ratio']} - Price-to-Book ratio compares a company's market value to its book value. A value under 1 may indicate an undervalued stock.")
        st.write(f"**EPS:** {company_info['EPS']} - Earnings per Share indicates the profitability of the company. Higher EPS means higher profitability.")
        st.write(f"**Revenue:** {company_info['Revenue']:,}" if company_info['Revenue'] != "N/A" else "**Revenue:** N/A")
        st.write(f"**Net Income:** {company_info['Net Income']:,}" if company_info['Net Income'] != "N/A" else "**Net Income:** N/A")
        st.write(f"**Debt to Equity Ratio:** {company_info['Debt to Equity']} - A measure of a company's financial leverage, calculated by dividing its total liabilities by shareholders' equity.")
        st.write(f"**Dividend Yield:** {company_info['Dividend Yield']} - The dividend yield shows how much cash flow you're getting for every dollar invested in an equity position.")
        st.write(f"**Profit Margin:** {company_info['Profit Margin']} - This shows how efficiently a company is converting its revenue into profits.")
        st.write(f"**Current Ratio:** {company_info['Current Ratio']} - A measure of a company’s ability to cover its short-term liabilities with its short-term assets.")
        st.write(f"**Quick Ratio:** {company_info['Quick Ratio']} - Similar to the current ratio but excludes inventory, providing a stricter view of a company's liquidity.")
        st.write(f"**ROE:** {company_info['ROE']} - Return on Equity shows how well a company uses investments to generate earnings growth.")

        # Recommendations based on metrics
        st.write("### Recommendation")
        recommendation = "Hold"
        description = "Fairly Valued"
        if company_info['PE Ratio'] != "N/A" and company_info['PE Ratio'] < 15:
            recommendation = "Buy"
            description = "Undervalued"
        elif company_info['PE Ratio'] != "N/A" and company_info['PE Ratio'] > 25:
            recommendation = "Sell"
            description = "Overvalued"
        
        st.write(f"**Recommendation:** {recommendation}")
        st.write(f"**Description:** {description}")

    elif analysis_type == "Technical Analysis":
        st.header("Technical Analysis")

        # Calculate indicators
        short_ma_days = st.sidebar.slider("Short-term moving average days:", 10, 100, 10)
        long_ma_days = st.sidebar.slider("Long-term moving average days:", 50, 200, 50)
        stock_data['SMA_Short'] = calculate_sma(stock_data, short_ma_days)
        stock_data['SMA_Long'] = calculate_sma(stock_data, long_ma_days)
        stock_data['RSI'] = calculate_rsi(stock_data, 20)
        stock_data['MACD'] = calculate_macd(stock_data)
        stock_data['UpperBB'], stock_data['MiddleBB'], stock_data['LowerBB'] = calculate_bollinger_bands(stock_data)
        stock_data['K'], stock_data['D'] = calculate_stochastic_oscillator(stock_data)

        # Plot charts
        st.write("### Price and Moving Averages")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['Close'], mode='lines', name="Close Price"))
        fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['SMA_Short'], mode='lines', name=f"SMA {short_ma_days}"))
        fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['SMA_Long'], mode='lines', name=f"SMA {long_ma_days}"))
        fig.update_layout(title="Close Price with SMA", template="plotly_dark")
        st.plotly_chart(fig)

        st.write("### Bollinger Bands")
        fig_bb = go.Figure()
        fig_bb.add_trace(go.Scatter(x=stock_data.index, y=stock_data['UpperBB'], mode='lines', name="Upper Band"))
        fig_bb.add_trace(go.Scatter(x=stock_data.index, y=stock_data['MiddleBB'], mode='lines', name="Middle Band"))
        fig_bb.add_trace(go.Scatter(x=stock_data.index, y=stock_data['LowerBB'], mode='lines', name="Lower Band"))
        fig_bb.update_layout(title="Bollinger Bands", template="plotly_dark")
        st.plotly_chart(fig_bb)

        st.write("### Stochastic Oscillator")
        fig_sto = go.Figure()
        fig_sto.add_trace(go.Scatter(x=stock_data.index, y=stock_data['K'], mode='lines', name="K"))
        fig_sto.add_trace(go.Scatter(x=stock_data.index, y=stock_data['D'], mode='lines', name="D"))
        fig_sto.update_layout(title="Stochastic Oscillator", template="plotly_dark")
        st.plotly_chart(fig_sto)

# Run the app
if __name__ == "__main__":
    main()
