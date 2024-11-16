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
    
    # Layout
    st.title(f"{info['longName']} ({ticker.upper()})")
    
    # Income Statement Section
    st.subheader("Income Statement")
    
    # Mock data for Income Statement
    # Replace this mock data with actual financials from yfinance or another API
    income_data = {
        "Year": ["2022", "2021", "2020"],
        "Total Revenue": [394.33, 365.82, 274.51],
        "COGS": [233.79, 219.32, 169.56],
        "Gross Profit": [160.54, 146.50, 104.95],
        "Operating Income": [119.34, 108.85, 66.29],
        "Pretax Income": [112.53, 100.56, 62.44],
        "Net Income": [95.11, 84.95, 57.41],
        "EBIT": [119.34, 108.85, 66.29],
        "EBITDA": [125.76, 114.65, 70.12],
        "ROE": [48.23, 45.61, 42.11]
    }
    income_df = pd.DataFrame(income_data)
    income_df.set_index("Year", inplace=True)

    # Plot Net Income, Total Revenue, and ROE
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=income_df.index,
            y=income_df["Net Income"],
            name="Net Income",
            marker=dict(color="blue"),
            yaxis="y1"
        )
    )
    fig.add_trace(
        go.Bar(
            x=income_df.index,
            y=income_df["Total Revenue"],
            name="Total Revenue",
            marker=dict(color="green"),
            yaxis="y1"
        )
    )
    fig.add_trace(
        go.Scatter(
            x=income_df.index,
            y=income_df["ROE"],
            name="ROE (%)",
            line=dict(color="red", width=2),
            yaxis="y2"
        )
    )

    # Configure the layout
    fig.update_layout(
        title="Income Statement Metrics",
        xaxis=dict(title="Year"),
        yaxis=dict(title="Amount (in billions USD)", side="left"),
        yaxis2=dict(
            title="ROE (%)",
            overlaying="y",
            side="right",
            showgrid=False
        ),
        legend=dict(x=0.01, y=0.99),
        barmode="group",
        template="plotly_white"
    )
    st.plotly_chart(fig)

    # Display Table
    st.subheader("Detailed Income Statement")
    st.table(income_df)

else:
    st.warning("Please enter a valid ticker symbol.")
