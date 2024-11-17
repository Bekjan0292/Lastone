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
    
    # Key Metrics Table
    st.subheader("Key Statistics")
    key_statistics_data = {
        "Metric": [
            "Current Price (USD)",
            "Market Cap (Billion USD)",
            "52-Week Low (USD)",
            "52-Week High (USD)"
        ],
        "Value": [
            f"{info.get('currentPrice', 'N/A'):.2f}" if info.get("currentPrice") else "N/A",
            f"{info.get('marketCap', 0) / 1e9:.2f}" if info.get("marketCap") else "N/A",
            f"{info.get('fiftyTwoWeekLow', 'N/A'):.2f}" if info.get("fiftyTwoWeekLow") else "N/A",
            f"{info.get('fiftyTwoWeekHigh', 'N/A'):.2f}" if info.get("fiftyTwoWeekHigh") else "N/A",
        ]
    }

    key_statistics_df = pd.DataFrame(key_statistics_data)

    # Display the table
    st.table(key_statistics_df)
    
    # Income Statement Section
    if st.button("View Income Statement"):
        st.subheader("Income Statement (Last 4 Years, in Millions USD)")
        financials = stock.financials.T
        balance_sheet = stock.balance_sheet.T

        # Check for missing or empty data
        if financials.empty or balance_sheet.empty:
            st.error("Financial or balance sheet data is not available for the selected stock.")
        else:
            # Convert index to years and sort
            financials.index = pd.to_datetime(financials.index).year
            balance_sheet.index = pd.to_datetime(balance_sheet.index).year
            financials = financials[financials.index != 2019].sort_index(ascending=False).head(4)
            
            # Extract required metrics
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
            
            # Add Profit Margin
            income_data["Profit Margin (%)"] = (income_data["Net Income"] / income_data["Total Revenue"] * 100).round(2)
            
            # Convert numeric columns to millions where appropriate
            for col in ["Total Revenue", "COGS", "Gross Profit", "Operating Income", "Pretax Income", "Net Income"]:
                income_data[col] = income_data[col].div(1e6).round(2)
            
            # Display Income Statement Table
            income_table = income_data.T
            income_table = income_table.applymap(lambda x: f"{x:,.2f}" if isinstance(x, (float, int)) else x)
            st.table(income_table)
        # Income Statement Graph with Dual Axes for Profit Margin
fig = go.Figure()

# Add Total Revenue (Left Axis)
fig.add_trace(
    go.Bar(
        x=income_data.index.astype(str),
        y=income_data["Total Revenue"],
        name="Total Revenue",
        marker=dict(color="indigo"),
        yaxis="y1"
    )
)

# Add Net Income (Left Axis)
fig.add_trace(
    go.Bar(
        x=income_data.index.astype(str),
        y=income_data["Net Income"],
        name="Net Income",
        marker=dict(color="orange"),
        yaxis="y1"
    )
)

# Calculate Profit Margin
profit_margin = (income_data["Net Income"] / income_data["Total Revenue"] * 100).round(2)

# Add Profit Margin (Right Axis)
fig.add_trace(
    go.Scatter(
        x=income_data.index.astype(str),
        y=profit_margin,
        name="Profit Margin (%)",
        line=dict(color="teal", width=3),
        yaxis="y2"
    )
)

# Update Layout for Dual Axes
fig.update_layout(
    title="Income Statement Metrics (Last 4 Years)",
    xaxis=dict(title="Year", type="category"),
    yaxis=dict(
        title="Amount (in millions USD)",
        titlefont=dict(color="black"),
        tickfont=dict(color="black"),
    ),
    yaxis2=dict(
        title="Profit Margin (%)",
        titlefont=dict(color="teal"),
        tickfont=dict(color="teal"),
        anchor="x",
        overlaying="y",
        side="right"
    ),
    barmode="group",
    template="plotly_white"
)
st.plotly_chart(fig)
# Recommendation Section
st.subheader("Recommendation")
pe_ratio = info.get("trailingPE", "N/A")
pb_ratio = info.get("priceToBook", "N/A")
de_ratio = info.get("debtToEquity", "N/A")
fcf = info.get("freeCashflow", "N/A")

# Placeholder for industry values (replace with actual data)
industry_pe = 20  # Example value for Industry P/E
industry_pb = 2.5  # Example value for Industry P/B
industry_de = 0.7  # Example value for Industry D/E
industry_fcf = "Positive"  # Example for Industry FCF (replace if numeric)

# Convert free cash flow to millions and format it
fcf_text = f"{(fcf / 1e6):,.2f}M USD" if isinstance(fcf, (int, float)) else "N/A"

# Define recommendations with explanations, pros, and cons
recommendation_data = [
    {
        "Metric": "P/E Ratio",
        "Current Value": f"{pe_ratio:.2f}" if isinstance(pe_ratio, (int, float)) else "N/A",
        "Industry Current Value": f"{industry_pe:.2f}" if isinstance(industry_pe, (int, float)) else "N/A",
        "Explanation": "The Price-to-Earnings (P/E) Ratio measures the stock price relative to its earnings. "
                       "A lower P/E indicates better value compared to earnings, but it can vary by industry.",
        "Pros": "Widely used; allows easy comparison with industry averages.",
        "Cons": "May be misleading for low-earning or high-growth companies.",
        "Recommendation": "Buy" if pe_ratio < 15 else "Hold" if 15 <= pe_ratio <= 25 else "Sell"
    },
    {
        "Metric": "P/B Ratio",
        "Current Value": f"{pb_ratio:.2f}" if isinstance(pb_ratio, (int, float)) else "N/A",
        "Industry Current Value": f"{industry_pb:.2f}" if isinstance(industry_pb, (int, float)) else "N/A",
        "Explanation": "The Price-to-Book (P/B) Ratio compares the stock price to the book value of the company. "
                       "Useful for determining undervalued or overvalued stocks in asset-heavy industries.",
        "Pros": "Effective for asset-heavy industries like real estate or manufacturing.",
        "Cons": "Less relevant for service-oriented or tech companies.",
        "Recommendation": "Buy" if pb_ratio < 1 else "Hold" if 1 <= pb_ratio <= 3 else "Sell"
    },
    {
        "Metric": "D/E Ratio",
        "Current Value": f"{de_ratio:.2f}" if isinstance(de_ratio, (int, float)) else "N/A",
        "Industry Current Value": f"{industry_de:.2f}" if isinstance(industry_de, (int, float)) else "N/A",
        "Explanation": "The Debt-to-Equity (D/E) Ratio evaluates a company's financial leverage by comparing its total debt "
                       "to shareholders' equity. A lower ratio indicates less financial risk.",
        "Pros": "Highlights the financial stability and leverage of the company.",
        "Cons": "Varies significantly by industry; may not always reflect operational risk.",
        "Recommendation": "Buy" if de_ratio < 0.5 else "Hold" if 0.5 <= de_ratio <= 1 else "Sell"
    },
    {
        "Metric": "Free Cash Flow (FCF)",
        "Current Value": fcf_text,
        "Industry Current Value": industry_fcf,  # Replace if numeric
        "Explanation": "Free Cash Flow (FCF) measures the cash a company generates after accounting for capital expenditures. "
                       "It reflects financial health and ability to fund growth or return value to shareholders.",
        "Pros": "Indicates financial health and growth potential.",
        "Cons": "Can fluctuate significantly year to year, especially in cyclical industries.",
        "Recommendation": "Buy" if isinstance(fcf, (int, float)) and fcf > 0 else "Sell"
    }
]

# Convert to DataFrame and display
recommendation_df = pd.DataFrame(recommendation_data)
st.table(recommendation_df)
