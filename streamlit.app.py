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
        financials = stock.financials.T
        financials.index = pd.to_datetime(financials.index).year
        income_data = financials[
            ["Total Revenue", "Cost Of Revenue", "Gross Profit", "Operating Income", "Pretax Income", "Net Income"]
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
        for col in ["Total Revenue", "COGS", "Gross Profit", "Operating Income", "Pretax Income", "Net Income", "EBIT", "EBITDA"]:
            income_data[col] = income_data[col].div(1e6).round(2)
        income_table = income_data.T
        income_table = income_table.applymap(lambda x: f"{x:,.2f}" if isinstance(x, (float, int)) else x)
        st.subheader("Income Statement (Last 5 Years, in Millions USD)")
        st.table(income_table)
        fig = go.Figure()
        fig.add_trace(
            go.Bar(
                x=income_data.index,
                y=income_data["Total Revenue"],
                name="Total Revenue",
                marker=dict(color="blue")
            )
        )
        fig.add_trace(
            go.Bar(
                x=income_data.index,
                y=income_data["Net Income"],
                name="Net Income",
                marker=dict(color="green")
            )
        )
        fig.add_trace(
            go.Scatter(
                x=income_data.index,
                y=income_data["EBITDA"],
                name="EBITDA",
                line=dict(color="red", width=2)
            )
        )
        fig.update_layout(
            title="Income Statement Metrics (Last 5 Years)",
            xaxis=dict(title="Year"),
            yaxis=dict(title="Amount (in millions USD)"),
            barmode="group",
            template="plotly_white"
        )
        st.plotly_chart(fig)
    
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
            title="Balance Sheet Metrics (Last 5 Years)",
            xaxis=dict(title="Year"),
            yaxis=dict(title="Amount (in millions USD)"),
            barmode="group",
            template="plotly_white"
        )
        st.plotly_chart(fig)
    
    # Recommendation Section
    with st.expander("View Recommendation"):
        # Fetch key financial ratios
        pe_ratio = info.get("trailingPE", "N/A")
        pb_ratio = info.get("priceToBook", "N/A")
        de_ratio = info.get("debtToEquity", "N/A")
        fcf = info.get("freeCashflow", "N/A")
        
        # Convert free cash flow to millions
        if fcf != "N/A" and fcf is not None:
            fcf = fcf / 1e6
            fcf = round(fcf, 2)
        
        # Define recommendations
        def get_recommendation(metric, value):
            if not isinstance(value, (int, float)):  # Handle non-numeric values
                return "N/A"
            if metric == "P/E":
                if value < 15:
                    return "Buy"
                elif 15 <= value <= 25:
                    return "Hold"
                else:
                    return "Sell"
            elif metric == "P/B":
                if value < 1:
                    return "Buy"
                elif 1 <= value <= 3:
                    return "Hold"
                else:
                    return "Sell"
            elif metric == "D/E":
                if value < 0.5:
                    return "Buy"
                elif 0.5 <= value <= 1:
                    return "Hold"
                else:
                    return "Sell"
            elif metric == "FCF":
                if value > 0:
                    return "Buy"
                else:
                    return "Sell"
            else:
                return "N/A"

        # Prepare data for the table
        recommendation_data = [
            ["P/E Ratio", pe_ratio, "Evaluates the stock's price relative to its earnings.", get_recommendation("P/E", pe_ratio)],
            ["P/B Ratio", pb_ratio, "Compares the stock's market price to book value.", get_recommendation("P/B", pb_ratio)],
            ["D/E Ratio", de_ratio, "Measures financial leverage (debt vs equity).", get_recommendation("D/E", de_ratio)],
            ["Free Cash Flow (FCF)", fcf, "Cash generated after capital expenses.", get_recommendation("FCF", fcf)],
        ]

        # Create a DataFrame
        recommendation_df = pd.DataFrame(recommendation_data, columns=["Metric", "Current Value", "Explanation", "Recommendation"])
        
        # Display the table
        st.subheader("Recommendation Table")
        st.table(recommendation_df)

else:
    st.warning("Please enter a valid ticker symbol.")
