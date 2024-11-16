import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd

# Page Config
st.set_page_config(page_title="Stock Fundamental Analysis", layout="wide")

# Sidebar
st.sidebar.title("Stock Analysis")
ticker = st.sidebar.text_input("Enter Stock Ticker:", value="AAPL")

# Fetch Data for Main Section
if ticker:
    stock = yf.Ticker(ticker)
    info = stock.info
    historical = stock.history(period="1y")
    
    # Layout
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
        yaxis_title="Price (USD)",
        template="plotly_white",
        hovermode="x",
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Balance Sheet Section
    with st.expander("View Balance Sheet"):
        balance_sheet = stock.balance_sheet.T
        balance_sheet.index = pd.to_datetime(balance_sheet.index).year
        balance_data = balance_sheet[
            ["Total Assets", "Total Liabilities Net Minority Interest", "Total Equity Gross Minority Interest"]
        ].copy()
        balance_data.rename(columns={
            "Total Assets": "Total Assets",
            "Total Liabilities Net Minority Interest": "Total Liabilities",
            "Total Equity Gross Minority Interest": "Total Equity"
        }, inplace=True)
        balance_data["Cash"] = balance_sheet.get("Cash And Cash Equivalents", 0)
        balance_data["Debt"] = balance_sheet.get("Short Long Term Debt Total", 0)
        balance_data["Working Capital"] = balance_data["Total Assets"] - balance_data["Total Liabilities"]
        balance_data = balance_data.tail(5).sort_index()
        for col in ["Total Assets", "Total Liabilities", "Total Equity", "Cash", "Debt", "Working Capital"]:
            balance_data[col] = balance_data[col].div(1e6).round(2)
        balance_table = balance_data.T
        balance_table = balance_table.applymap(lambda x: f"{x:,.2f}" if isinstance(x, (float, int)) else x)
        st.subheader("Balance Sheet (Last 5 Years, in Millions USD)")
        st.table(balance_table)
        fig = go.Figure()
        fig.add_trace(
            go.Bar(
                x=balance_data.index,
                y=balance_data["Total Assets"],
                name="Total Assets",
                marker=dict(color="blue")
            )
        )
        fig.add_trace(
            go.Bar(
                x=balance_data.index,
                y=balance_data["Total Liabilities"],
                name="Total Liabilities",
                marker=dict(color="red")
            )
        )
        fig.add_trace(
            go.Bar(
                x=balance_data.index,
                y=balance_data["Total Equity"],
                name="Total Equity",
                marker=dict(color="green")
            )
        )
        fig.update_layout(
            title="Balance Sheet Metrics (5 Years)",
            xaxis=dict(title="Year"),
            yaxis=dict(title="Amount (in millions USD)"),
            barmode="group",
            template="plotly_white"
        )
        st.plotly_chart(fig)
    
    # Cash Flow Section
    with st.expander("View Cash Flow Statement"):
        cash_flow = stock.cashflow.T
        cash_flow.index = pd.to_datetime(cash_flow.index).year
        cash_flow_data = cash_flow[
            ["Total Cash From Operating Activities", "Total Cashflows From Investing Activities", "Total Cash From Financing Activities"]
        ].copy()
        cash_flow_data.rename(columns={
            "Total Cash From Operating Activities": "Operating Cash Flow",
            "Total Cashflows From Investing Activities": "Investing Cash Flow",
            "Total Cash From Financing Activities": "Financing Cash Flow"
        }, inplace=True)
        cash_flow_data = cash_flow_data.tail(5).sort_index()
        for col in ["Operating Cash Flow", "Investing Cash Flow", "Financing Cash Flow"]:
            cash_flow_data[col] = cash_flow_data[col].div(1e6).round(2)
        cash_flow_table = cash_flow_data.T
        cash_flow_table = cash_flow_table.applymap(lambda x: f"{x:,.2f}" if isinstance(x, (float, int)) else x)
        st.subheader("Cash Flow Statement (Last 5 Years, in Millions USD)")
        st.table(cash_flow_table)
        fig = go.Figure()
        fig.add_trace(
            go.Bar(
                x=cash_flow_data.index,
                y=cash_flow_data["Operating Cash Flow"],
                name="Operating Cash Flow",
                marker=dict(color="blue")
            )
        )
        fig.add_trace(
            go.Bar(
                x=cash_flow_data.index,
                y=cash_flow_data["Investing Cash Flow"],
                name="Investing Cash Flow",
                marker=dict(color="red")
            )
        )
        fig.add_trace(
            go.Bar(
                x=cash_flow_data.index,
                y=cash_flow_data["Financing Cash Flow"],
                name="Financing Cash Flow",
                marker=dict(color="green")
            )
        )
        fig.update_layout(
            title="Cash Flow Statement Metrics (5 Years)",
            xaxis=dict(title="Year"),
            yaxis=dict(title="Amount (in millions USD)"),
            barmode="group",
            template="plotly_white"
        )
        st.plotly_chart(fig)

else:
    st.warning("Please enter a valid ticker symbol.")
