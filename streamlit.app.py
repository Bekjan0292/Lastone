import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(page_title="Enhanced Portfolio Analysis Dashboard", layout="wide")

# App title
st.title("📊 Enhanced Portfolio Analysis Dashboard")

# Sidebar for input
st.sidebar.header("Input Parameters")
ticker_list = st.sidebar.text_input("Enter ticker symbols (e.g., AAPL, MSFT, TSLA)", value="AAPL, MSFT")
tickers = [ticker.strip().upper() for ticker in ticker_list.split(",")]

@st.cache_data
def fetch_portfolio_data(tickers):
    """Fetches historical data for the tickers."""
    return yf.download(" ".join(tickers), period="6mo", group_by='ticker')  # Shorter period for faster load

portfolio_data = fetch_portfolio_data(tickers)

# Portfolio Overview Section
st.header("Portfolio Overview")

if not portfolio_data.empty:
    col1, col2, col3 = st.columns(3)

    with col1:
        # Total Value Calculation
        total_value = sum([portfolio_data[ticker]["Close"].iloc[-1] for ticker in tickers])
        st.metric("💰 Total Value", f"${total_value:,.2f}")

    with col2:
        # Total Returns Calculation
        total_returns = sum([(portfolio_data[ticker]["Close"].iloc[-1] - portfolio_data[ticker]["Close"].iloc[0]) / portfolio_data[ticker]["Close"].iloc[0] * 100
                             for ticker in tickers])
        st.metric("📈 Total Returns", f"{total_returns / len(tickers):.2f}%")

    @st.cache_data
    def get_dividend_yield(ticker):
        """Fetches dividend yield for a single ticker."""
        stock = yf.Ticker(ticker)
        return stock.info.get("dividendYield", 0)

    avg_dividend_yield = sum(get_dividend_yield(ticker) for ticker in tickers) / len(tickers)
    with col3:
        st.metric("💸 Est. Dividend Yield", f"{avg_dividend_yield:.2f}%")

    # Performance Chart
    st.subheader("Performance Over Time")
    performance_fig = go.Figure()
    for ticker in tickers:
        performance_fig.add_trace(go.Scatter(x=portfolio_data[ticker].index, y=portfolio_data[ticker]["Close"], mode='lines', name=ticker))
    performance_fig.update_layout(title="Portfolio Performance Over Time", yaxis_title="Stock Price", xaxis_title="Date")
    st.plotly_chart(performance_fig, use_container_width=True)

    # Financial Health - Radar Chart
    st.subheader("Financial Health Snapshot")
    categories = ["Dividend", "Value", "Future", "Health", "Past"]
    sample_values = [3, 4, 2, 5, 3]  # Placeholder values; replace with calculations if available
    radar_fig = go.Figure(data=go.Scatterpolar(r=sample_values, theta=categories, fill='toself'))
    radar_fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 5])), showlegend=False)
    st.plotly_chart(radar_fig, use_container_width=True)

    # Dividend Analysis
    st.subheader("Dividend Analysis")
    dividend_col1, dividend_col2 = st.columns(2)
    with dividend_col1:
        st.metric("🔮 Expected Dividends (Next 12M)", f"${avg_dividend_yield * total_value:.2f}")
    with dividend_col2:
        yield_on_cost = avg_dividend_yield * 100
        st.metric("📉 Yield on Cost", f"{yield_on_cost:.2f}%")

    # Growth Forecasts (Sample Data)
    st.subheader("Growth Forecasts Comparison")
    forecast_data = pd.DataFrame({
        "Metric": ["Earnings Growth (next 3 years)", "Revenue Growth (next 3 years)", "Return on Equity (next 3 years)"],
        "Company": [5.2, 6.1, 8.4],
        "Industry": [4.5, 5.7, 7.8],
        "Market": [7.5, 6.9, 10.2]
    })
    growth_fig = px.bar(forecast_data, x="Metric", y=["Company", "Industry", "Market"], barmode="group",
                        title="Growth Forecasts Comparison")
    st.plotly_chart(growth_fig, use_container_width=True)

    # Management & Key Information
    st.subheader("Management & Key Information")
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        st.write(f"### {ticker} - {stock.info.get('longName', 'Company Name Not Available')}")
        st.write(f"CEO: {stock.info.get('ceo', 'N/A')}")
        st.write(f"Market Cap: {stock.info.get('marketCap', 'Data Not Available')}")
        st.write("---")
else:
    st.warning("No valid portfolio data available.")

# Footer with additional info or company links
st.sidebar.write("Data provided by Yahoo Finance")
