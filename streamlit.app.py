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

# Initialize session state for the stock ticker
if "ticker" not in st.session_state:
    st.session_state["ticker"] = ""

# Starting Page
def starting_page():
    st.title("Stock Analyzer")
    st.write("Welcome to the Stock Analyzer! Analyze stocks both fundamentally and technically.")

    # Input stock ticker
    ticker = st.text_input("Enter Stock Ticker (e.g., AAPL, TSLA):", value=st.session_state["ticker"])
    st.session_state["ticker"] = ticker

    # Buttons to choose analysis type
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Go to Fundamental Analysis"):
            st.session_state["page"] = "Fundamental"
    with col2:
        if st.button("Go to Technical Analysis"):
            st.session_state["page"] = "Technical"

# Fundamental Analysis Page
def fundamental_analysis():
    st.title("Fundamental Analysis")

    if "ticker" not in st.session_state or not st.session_state["ticker"]:
        st.warning("Please go back to the starting page and enter a stock ticker.")
        return

    ticker = st.session_state["ticker"]
    stock = yf.Ticker(ticker)
    info = stock.info

    # Company Details
    st.subheader(f"Company: {info.get('longName', 'Unknown')} ({ticker})")
    st.markdown(f"**Sector**: {info.get('sector', 'N/A')}")
    st.markdown(f"**Industry**: {info.get('industry', 'N/A')}")

    # Financial Metrics
    st.subheader("Key Financial Metrics")
    metrics = {
        "Market Cap": f"${info.get('marketCap', 0):,}",
        "Price to Earnings (PE) Ratio (TTM)": info.get('forwardPE', 'N/A'),
        "Dividend Yield": f"{info.get('dividendYield', 0) * 100:.2f}%",
        "52-Week High": f"${info.get('fiftyTwoWeekHigh', 'N/A')}",
        "52-Week Low": f"${info.get('fiftyTwoWeekLow', 'N/A')}"
    }
    metrics_df = pd.DataFrame(metrics.items(), columns=["Metric", "Value"])

    # Fix mixed types in the Value column
    metrics_df["Value"] = metrics_df["Value"].astype(str)
    st.table(metrics_df)

    # Interactive Revenue and Net Income Chart
    st.subheader("Revenue and Net Income (Interactive)")
    try:
        financials = stock.financials.T
        financials = financials.rename(columns={
            "Total Revenue": "Revenue",
            "Net Income": "Net Income"
        })
        chart_data = financials[["Revenue", "Net Income"]].reset_index()
        chart_data = chart_data.melt(id_vars="index", var_name="Metric", value_name="Amount")

        fig = px.line(
            chart_data,
            x="index",
            y="Amount",
            color="Metric",
            title="Revenue and Net Income Trends",
            labels={"index": "Year", "Amount": "Amount (USD)", "Metric": "Metric"}
        )
        st.plotly_chart(fig)
    except Exception:
        st.warning("Unable to fetch financial history data.")

    # Recommendation Visualization
    st.subheader("Recommendation")
    recommendation = "Hold"
    pe = info.get("forwardPE", None)
    if pe:
        if pe < 15:
            recommendation = "Buy"
        elif pe > 25:
            recommendation = "Sell"

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=pe if pe else 20,
        title={"text": f"PE Ratio ({recommendation})"},
        gauge={
            "axis": {"range": [0, 40]},
            "bar": {"color": "green" if recommendation == "Buy" else "red" if recommendation == "Sell" else "yellow"}
        }
    ))
    st.plotly_chart(fig)

    # Back button to navigate to the Main Page
    if st.button("Back to Main Page"):
        st.session_state["page"] = "Start"

# Technical Analysis Placeholder
def technical_analysis():
    st.title("Technical Analysis")
    st.write("Technical analysis functionality will go here.")

    # Back button to navigate to the Main Page
    if st.button("Back to Main Page"):
        st.session_state["page"] = "Start"

# Navigation Logic
if "page" not in st.session_state:
    st.session_state["page"] = "Start"

if st.session_state["page"] == "Start":
    starting_page()
elif st.session_state["page"] == "Fundamental":
    fundamental_analysis()
elif st.session_state["page"] == "Technical":
    technical_analysis()
