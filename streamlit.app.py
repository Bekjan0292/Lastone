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

def fundamental_analysis_page():
    st.title("Fundamental Analysis")

    if not st.session_state["stock_data"]:
        st.warning("Please go back to the main page and enter a stock ticker.")
        return

    # Retrieve data from session_state
    info, financials, history = st.session_state["stock_data"]

    # Company Overview
    st.subheader(f"Company Overview: {info.get('longName', 'Unknown')} ({st.session_state['ticker']})")
    st.write(f"**Sector:** {info.get('sector', 'N/A')} | **Industry:** {info.get('industry', 'N/A')}")
    st.write(f"**Business Model:** {info.get('longBusinessSummary', 'N/A')}")

    # Quantitative Analysis
    st.subheader("Quantitative Analysis")

    # Income Statement
    st.markdown("### Income Statement")
    try:
        st.write("**Revenue and Net Income Trends:**")
        financials = financials.rename(columns={"Total Revenue": "Revenue", "Net Income": "Net Income"})
        income_data = financials[["Revenue", "Net Income"]].reset_index()
        income_data = income_data.melt(id_vars="index", var_name="Metric", value_name="Amount")
        fig = px.line(
            income_data,
            x="index",
            y="Amount",
            color="Metric",
            title="Income Trends",
            labels={"index": "Year", "Amount": "Amount (USD)", "Metric": "Metric"}
        )
        st.plotly_chart(fig)
    except Exception:
        st.warning("Unable to retrieve Income Statement data.")

    # Balance Sheet Metrics
    st.markdown("### Balance Sheet")
    try:
        balance_sheet_metrics = {
            "Total Assets": info.get('totalAssets', 'N/A'),
            "Total Liabilities": info.get('totalLiabilities', 'N/A'),
            "Debt-to-Equity Ratio": info.get('debtToEquity', 'N/A'),
        }
        balance_sheet_df = pd.DataFrame(balance_sheet_metrics.items(), columns=["Metric", "Value"])
        balance_sheet_df["Value"] = balance_sheet_df["Value"].astype(str)
        st.table(balance_sheet_df)
    except Exception:
        st.warning("Unable to retrieve Balance Sheet data.")

    # Cash Flow Statement
    st.markdown("### Cash Flow Statement")
    try:
        cash_flow_metrics = {
            "Cash Flow from Operations": info.get('operatingCashflow', 'N/A'),
            "Free Cash Flow": info.get('freeCashflow', 'N/A'),
        }
        cash_flow_df = pd.DataFrame(cash_flow_metrics.items(), columns=["Metric", "Value"])
        cash_flow_df["Value"] = cash_flow_df["Value"].astype(str)
        st.table(cash_flow_df)
    except Exception:
        st.warning("Unable to retrieve Cash Flow data.")

    # Qualitative Analysis
    st.subheader("Qualitative Analysis")

    # Competitive Advantage
    st.markdown("### Competitive Advantage")
    st.write(f"**Market Cap:** ${info.get('marketCap', 0):,}")
    st.write("Evaluate the company's competitive position and potential for long-term growth.")

    # Management
    st.markdown("### Management")
    st.write(f"**CEO:** {info.get('ceo', 'N/A')}")
    st.write("Assess the leadership and governance structure of the company.")

    # Sector Trends
    st.markdown("### Sector Trends")
    st.write(f"The company operates in the **{info.get('sector', 'N/A')}** sector and is part of the **{info.get('industry', 'N/A')}** industry.")
    st.write("Analyze sector performance and how the company aligns with industry trends.")

    # Recommendation
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
