import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set up page configuration
st.set_page_config(
    page_title="Stock Analyzer",
    page_icon="📊",
    layout="wide"
)

# Caching data using @st.cache_data
@st.cache_data
def get_stock_data(ticker):
    stock = yf.Ticker(ticker)
    return stock.info, stock.financials.T, stock.history(period="5y")

# Initialize session_state for ticker and current page
if "ticker" not in st.session_state:
    st.session_state["ticker"] = ""
if "page" not in st.session_state:
    st.session_state["page"] = "Main"
if "stock_data" not in st.session_state:
    st.session_state["stock_data"] = None

# Main Page
def main_page():
    st.title("Stock Analyzer")
    st.write("Welcome! Analyze stocks both fundamentally and technically.")

    # Input field for stock ticker
    ticker = st.text_input("Enter Stock Ticker (e.g., AAPL, TSLA):", value=st.session_state["ticker"])
    st.session_state["ticker"] = ticker

    # Buttons for navigation
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Go to Fundamental Analysis") and ticker:
            # Load and store data in session_state
            st.session_state["stock_data"] = get_stock_data(ticker)
            st.session_state["page"] = "Fundamental"
    with col2:
        if st.button("Go to Technical Analysis") and ticker:
            st.session_state["stock_data"] = get_stock_data(ticker)
            st.session_state["page"] = "Technical"

# Fundamental Analysis Page
def fundamental_analysis_page():
    st.title("Fundamental Analysis")

    # Check if data exists
    if not st.session_state["stock_data"]:
        st.warning("Please go back to the main page and enter a stock ticker.")
        return

    # Retrieve data from session_state
    info, financials, history = st.session_state["stock_data"]

    # Company Information
    st.subheader(f"Company: {info.get('longName', 'Unknown')} ({st.session_state['ticker']})")
    st.write(f"**Sector:** {info.get('sector', 'N/A')} | **Industry:** {info.get('industry', 'N/A')}")

    # Key Metrics
    st.subheader("Key Financial Metrics")
    metrics = {
        "Market Cap": f"${info.get('marketCap', 0):,}",
        "P/E Ratio (TTM)": info.get('forwardPE', 'N/A'),
        "Dividend Yield": f"{info.get('dividendYield', 0) * 100:.2f}%",
        "52-Week High": f"${info.get('fiftyTwoWeekHigh', 'N/A')}",
        "52-Week Low": f"${info.get('fiftyTwoWeekLow', 'N/A')}"
    }
    metrics_df = pd.DataFrame(metrics.items(), columns=["Metric", "Value"])

    # Fix Arrow serialization issue by converting to strings
    metrics_df["Value"] = metrics_df["Value"].astype(str)
    st.table(metrics_df)

    # Revenue and Net Income Chart
    st.subheader("Revenue and Net Income (Interactive)")
    try:
        financials = financials.rename(columns={"Total Revenue": "Revenue", "Net Income": "Net Income"})
        financials_chart = financials[["Revenue", "Net Income"]].reset_index()
        financials_chart = financials_chart.melt(id_vars="index", var_name="Metric", value_name="Amount")
        fig = px.line(
            financials_chart,
            x="index",
            y="Amount",
            color="Metric",
            title="Revenue and Net Income Trends",
            labels={"index": "Year", "Amount": "Amount (USD)"}
        )
        st.plotly_chart(fig)
    except Exception:
        st.warning("Unable to load financial data.")

    # Recommendation
    st.subheader("Recommendation")
    recommendation = "Hold"
    pe = info.get("forwardPE", None)
    if pe:
        if pe < 15:
            recommendation = "Buy"
        elif pe > 25:
            recommendation = "Sell"

    # Gauge Chart for Recommendation
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=pe if pe else 20,
        title={"text": f"P/E Ratio ({recommendation})"},
        gauge={
            "axis": {"range": [0, 40]},
            "bar": {"color": "green" if recommendation == "Buy" else "red" if recommendation == "Sell" else "yellow"}
        }
    ))
    st.plotly_chart(fig)

    # Back button
    if st.button("Back to Main Page"):
        st.session_state["page"] = "Main"

# Technical Analysis Page (Placeholder)
def technical_analysis_page():
    st.title("Technical Analysis")
    st.write("Technical analysis functionality will be implemented here.")

    # Back button
    if st.button("Back to Main Page"):
        st.session_state["page"] = "Main"

# Navigation between pages
if st.session_state["page"] == "Main":
    main_page()
elif st.session_state["page"] == "Fundamental":
    fundamental_analysis_page()
elif st.session_state["page"] == "Technical":
    technical_analysis_page()
