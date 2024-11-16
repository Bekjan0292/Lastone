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
    
    # Income Statement Section
    with st.expander("View Income Statement"):
        # Fetch financial data
        financials = stock.financials.T
        financials.index = pd.to_datetime(financials.index).year  # Convert to year format
        
        # Select relevant metrics and prepare data
        income_data = financials[
            ["Total Revenue", "Cost Of Revenue", "Gross Profit", "Operating Income",
             "Pretax Income", "Net Income"]
        ].copy()
        income_data.rename(columns={
            "Total Revenue": "Total Revenue",
            "Cost Of Revenue": "COGS",
            "Gross Profit": "Gross Profit",
            "Operating Income": "Operating Income",
            "Pretax Income": "Pretax Income",
            "Net Income": "Net Income"
        }, inplace=True)
        income_data["EBIT"] = income_data["Operating Income"]
        income_data["EBITDA"] = income_data["Operating Income"] + financials.get("Depreciation", 0)
        
        # Ensure data is for the last 5 years
        income_data = income_data.tail(5).sort_index()

        # Add mock ROE data (replace with real calculation if available)
        income_data["ROE"] = [48.23, 45.61, 42.11, 38.95, 35.12]  # Placeholder values

        # Graph for Net Income, Total Revenue, and ROE
        fig = go.Figure()
        fig.add_trace(
            go.Bar(
                x=income_data.index,
                y=income_data["Net Income"] / 1e9,  # Convert to billions
                name="Net Income",
                marker=dict(color="blue"),
                yaxis="y1"
            )
        )
        fig.add_trace(
            go.Bar(
                x=income_data.index,
                y=income_data["Total Revenue"] / 1e9,  # Convert to billions
                name="Total Revenue",
                marker=dict(color="green"),
                yaxis="y1"
            )
        )
        fig.add_trace(
            go.Scatter(
                x=income_data.index,
                y=income_data["ROE"],
                name="ROE (%)",
                line=dict(color="red", width=2),
                yaxis="y2"
            )
        )

        # Configure the layout
        fig.update_layout(
            title="Income Statement Metrics (5 Years)",
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

        # Transpose table: Switch rows and columns
        st.subheader("Detailed Income Statement")
        income_table = income_data.T
        st.table(income_table)

else:
    st.warning("Please enter a valid ticker symbol.")
