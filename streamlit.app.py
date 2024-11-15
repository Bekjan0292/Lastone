import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import ta

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
        st.write(f"**Profit Margin:** {company_info['Profit Margin']}")
        st.write(f"**Current Ratio:** {company_info['Current Ratio']}")
        st.write(f"**Quick Ratio:** {company_info['Quick Ratio']}")
        st.write(f"**ROE:** {company_info['ROE']}")

        # Recommendations (Example logic, can be expanded based on user preference)
        st.write("### Recommendation")
        if company_info['PE Ratio'] != "N/A" and company_info['PE Ratio'] < 15:
            recommendation = "Buy"
            description = "Undervalued"
        elif company_info['PE Ratio'] != "N/A" and company_info['PE Ratio'] > 25:
            recommendation = "Sell"
            description = "Overvalued"
        else:
            recommendation = "Hold"
            description = "Fairly Valued"

        st.write(f"**Recommendation:** {recommendation}")
        st.write(f"**Description:** {description}")

    elif analysis_type == "Technical Analysis":
        st.header("Technical Analysis")

        # Calculate indicators using `ta` library
        short_ma_days = st.sidebar.slider("Short-term moving average days:", 10, 100, 10)
        long_ma_days = st.sidebar.slider("Long-term moving average days:", 50, 200, 50)

        # Calculate moving averages, RSI, MACD, Bollinger Bands, and Stochastic Oscillator
        stock_data['SMA_Short'] = ta.trend.sma_indicator(stock_data['Close'], window=short_ma_days)
        stock_data['SMA_Long'] = ta.trend.sma_indicator(stock_data['Close'], window=long_ma_days)
        stock_data['RSI'] = ta.momentum.rsi(stock_data['Close'], window=14)
        stock_data['MACD'] = ta.trend.macd(stock_data['Close'])
        stock_data['MACD_signal'] = ta.trend.macd_signal(stock_data['Close'])
        stock_data['UpperBB'], stock_data['MiddleBB'], stock_data['LowerBB'] = ta.volatility.bollinger_bands(stock_data['Close'])
        stock_data['K'], stock_data['D'] = ta.momentum.stochastic_oscillator(stock_data['High'], stock_data['Low'], stock_data['Close'])

        # Plot charts
        st.write("### Price and Moving Averages")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['Close'], mode='lines', name="Close Price"))
        fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['SMA_Short'], mode='lines', name=f"SMA {short_ma_days}"))
        fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['SMA_Long'], mode='lines', name=f"SMA {long_ma_days}"))
        fig.update_layout(title=f"Close Price with SMA {short_ma_days} and SMA {long_ma_days}", template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

        st.write("### Bollinger Bands")
        fig_bb = go.Figure()
        fig_bb.add_trace(go.Scatter(x=stock_data.index, y=stock_data['UpperBB'], mode='lines', name="Upper BB"))
        fig_bb.add_trace(go.Scatter(x=stock_data.index, y=stock_data['MiddleBB'], mode='lines', name="Middle BB"))
        fig_bb.add_trace(go.Scatter(x=stock_data.index, y=stock_data['LowerBB'], mode='lines', name="Lower BB"))
        fig_bb.update_layout(title="Bollinger Bands", template="plotly_dark")
        st.plotly_chart(fig_bb, use_container_width=True)

        st.write("### Stochastic Oscillator")
        fig_stochastic = go.Figure()
        fig_stochastic.add_trace(go.Scatter(x=stock_data.index, y=stock_data['K'], mode='lines', name="%K"))
        fig_stochastic.add_trace(go.Scatter(x=stock_data.index, y=stock_data['D'], mode='lines', name="%D"))
        fig_stochastic.update_layout(title="Stochastic Oscillator", template="plotly_dark")
        st.plotly_chart(fig_stochastic, use_container_width=True)

        # RSI
        st.write("### RSI")
        fig_rsi = go.Figure()
        fig_rsi.add_trace(go.Scatter(x=stock_data.index, y=stock_data['RSI'], mode='lines', name="RSI"))
        fig_rsi.update_layout(title="RSI (14)", template="plotly_dark")
        st.plotly_chart(fig_rsi, use_container_width=True)

        # MACD
        st.write("### MACD")
        fig_macd = go.Figure()
        fig_macd.add_trace(go.Scatter(x=stock_data.index, y=stock_data['MACD'], mode='lines', name="MACD"))
        fig_macd.add_trace(go.Scatter(x=stock_data.index, y=stock_data['MACD_signal'], mode='lines', name="MACD Signal"))
        fig_macd.update_layout(title="MACD", template="plotly_dark")
        st.plotly_chart(fig_macd, use_container_width=True)

if __name__ == "__main__":
    main()
