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
    
    # Key statistics with explanations
    st.subheader("Key Statistics")
    stats_data = [
        ["Current Price", f"${info['currentPrice']:.2f}", "The current trading price of the stock."],
        ["Market Cap", f"${info['marketCap'] / 1e9:,.2f}B", "The total value of the company based on its stock price and shares outstanding."],
        ["52W Range", f"{info['fiftyTwoWeekLow']:.2f} - {info['fiftyTwoWeekHigh']:.2f}", "The range of the stock price over the last 52 weeks."],
        ["Previous Close", f"${info['previousClose']:.2f}", "The last recorded closing price of the stock."],
        ["Open", f"${info['open']:.2f}", "The stock price at the start of the trading session."],
        ["Day's Range", f"{info['dayLow']:.2f} - {info['dayHigh']:.2f}", "The lowest and highest price during today's trading session."],
        ["Beta", f"{info['beta']:.2f}", "A measure of the stock's volatility compared to the overall market."],
        ["P/E Ratio", f"{info.get('trailingPE', 'N/A'):.2f}" if info.get('trailingPE') else "N/A", "The price-to-earnings ratio, showing the price relative to earnings per share."],
        ["P/B Ratio", f"{info.get('priceToBook', 'N/A'):.2f}" if info.get('priceToBook') else "N/A", "The price-to-book ratio, showing the price relative to book value per share."],
        ["EPS", f"{info.get('trailingEps', 'N/A'):.2f}" if info.get('trailingEps') else "N/A", "Earnings per share, showing profit allocated to each outstanding share."]
    ]
    
    # Create a DataFrame for better display
    stats_df = pd.DataFrame(stats_data, columns=["Metric", "Value", "Explanation"])
    st.table(stats_df)
    
    
# Income Statement Section
income_data["Profit Margin (%)"] = (income_data["Net Income"] / income_data["Total Revenue"] * 100).round(2)

# Convert numeric columns to millions where appropriate
for col in ["Total Revenue", "COGS", "Gross Profit", "Operating Income", "Pretax Income", "Net Income"]:
    income_data[col] = income_data[col].div(1e6).round(2)

income_table = income_data.T
income_table = income_table.applymap(lambda x: f"{x:,.2f}" if isinstance(x, (float, int)) else x)
st.table(income_table)
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
            financials = financials[financials.index != 2019].sort_index(ascending=False).head(4)  # Exclude 2019
            balance_sheet = balance_sheet[balance_sheet.index != 2019].sort_index(ascending=False).head(4)  # Exclude 2019
            
            # Extract required metrics
            total_assets = balance_sheet["Total Assets"]
            total_equity = balance_sheet["Total Equity Gross Minority Interest"]
            net_income = financials["Net Income"]

            # Calculate ROA and ROE
            roa = (net_income / total_assets * 100).round(2)
            roe = (net_income / total_equity * 100).round(2)

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
            income_data["ROA (%)"] = roa
            income_data["ROE (%)"] = roe

            for col in ["Total Revenue", "COGS", "Gross Profit", "Operating Income", "Pretax Income", "Net Income"]:
                income_data[col] = income_data[col].div(1e6).round(2)
            
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

# Add Profit Margin (Right Axis)
profit_margin = (income_data["Net Income"] / income_data["Total Revenue"] * 100).round(2)
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
 for Profit Margin
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

# Add Profit Margin (Right Axis)
profit_margin = (income_data["Net Income"] / income_data["Total Revenue"] * 100).round(2)
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

            # Add ROE (Right Axis)
            fig.add_trace(
                go.Scatter(
                    x=income_data.index.astype(str),
                    y=income_data["ROE (%)"],
                    name="ROE (%)",
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
                    title="ROE (%)",
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
    
    # Balance Sheet Section
    if st.button("View Balance Sheet"):
        st.subheader("Balance Sheet (Last 4 Years, in Millions USD)")

        # Fetch balance sheet data
        balance_sheet = stock.balance_sheet.T  # Transpose for easier row handling
        if balance_sheet.empty:
            st.error("Balance sheet data is not available for the selected stock.")
        else:
            # Convert index to years
            balance_sheet.index = pd.to_datetime(balance_sheet.index).year

            # Remove 2019 and keep only the last 4 years
            balance_sheet = balance_sheet.sort_index(ascending=False).head(4)

            # Extract key metrics
            balance_data = balance_sheet[
                ["Total Assets", "Total Liabilities Net Minority Interest", "Total Equity Gross Minority Interest"]
            ].copy()
            balance_data.rename(columns={
                "Total Assets": "Total Assets",
                "Total Liabilities Net Minority Interest": "Total Liabilities",
                "Total Equity Gross Minority Interest": "Total Equity"
            }, inplace=True)

            # Add derived metrics
            balance_data["Cash"] = balance_sheet.get("Cash And Cash Equivalents", 0)
            balance_data["Debt"] = balance_sheet.get("Short Long Term Debt Total", 0)
            balance_data["Working Capital"] = balance_data["Total Assets"] - balance_data["Total Liabilities"]

            # Format data
            for col in ["Total Assets", "Total Liabilities", "Total Equity", "Cash", "Debt", "Working Capital"]:
                balance_data[col] = balance_data[col].div(1e6).round(2)

            # Display table
            balance_table = balance_data.T
            balance_table = balance_table.applymap(lambda x: f"{x:,.2f}" if isinstance(x, (float, int)) else x)
            st.table(balance_table)

            # Plot Balance Sheet Metrics
            fig = go.Figure()
            fig.add_trace(
                go.Bar(
                    x=balance_data.index.astype(str),
                    y=balance_data["Total Assets"],
                    name="Total Assets",
                    marker=dict(color="purple")
                )
            )
            fig.add_trace(
                go.Bar(
                    x=balance_data.index.astype(str),
                    y=balance_data["Total Liabilities"],
                    name="Total Liabilities",
                    marker=dict(color="red")
                )
            )
            fig.add_trace(
                go.Bar(
                    x=balance_data.index.astype(str),
                    y=balance_data["Total Equity"],
                    name="Total Equity",
                    marker=dict(color="green")
                )
            )
            fig.update_layout(
                title="Balance Sheet Metrics (Last 4 Years)",
                xaxis=dict(title="Year", type="category"),
                yaxis=dict(title="Amount (in millions USD)"),
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

# Convert free cash flow to millions and format it
fcf_text = f"{(fcf / 1e6):,.2f}M USD" if isinstance(fcf, (int, float)) else "N/A"

# Define recommendations with pros, cons, and thresholds
recommendation_data = [
    {
        "Metric": "P/E Ratio",
        "Current Value": f"{pe_ratio:.2f}" if isinstance(pe_ratio, (int, float)) else "N/A",
        "Pros": "Widely used; easy comparison with industry.",
        "Cons": "May be misleading for low-earning companies.",
        "Threshold": "Below 15: Buy; 15-25: Hold; Above 25: Sell"
    },
    {
        "Metric": "P/B Ratio",
        "Current Value": f"{pb_ratio:.2f}" if isinstance(pb_ratio, (int, float)) else "N/A",
        "Pros": "Useful for asset-heavy industries.",
        "Cons": "Less relevant for tech or service companies.",
        "Threshold": "Below 1: Buy; 1-3: Hold; Above 3: Sell"
    },
    {
        "Metric": "D/E Ratio",
        "Current Value": f"{de_ratio:.2f}" if isinstance(de_ratio, (int, float)) else "N/A",
        "Pros": "Indicates financial leverage and risk.",
        "Cons": "Varies significantly by industry.",
        "Threshold": "Below 0.5: Buy; 0.5-1: Hold; Above 1: Sell"
    },
    {
        "Metric": "Free Cash Flow (FCF)",
        "Current Value": fcf_text,
        "Pros": "Indicates financial health and growth potential.",
        "Cons": "Can fluctuate significantly year to year.",
        "Threshold": "Positive: Buy; Negative: Sell"
    }
]

# Convert to DataFrame and display
recommendation_df = pd.DataFrame(recommendation_data)
st.table(recommendation_df)

st.subheader("Recommendation")
pe_ratio = info.get("trailingPE", "N/A")
pb_ratio = info.get("priceToBook", "N/A")
de_ratio = info.get("debtToEquity", "N/A")
fcf = info.get("freeCashflow", "N/A")

# Convert free cash flow to millions and format it
fcf_text = f"{(fcf / 1e6):,.2f}M USD" if isinstance(fcf, (int, float)) else "N/A"

# Define recommendations with pros, cons, and thresholds
recommendation_data = [
    {
        "Metric": "P/E Ratio",
        "Current Value": f"{pe_ratio:.2f}" if isinstance(pe_ratio, (int, float)) else "N/A",
        "Pros": "Widely used; easy comparison with industry.",
        "Cons": "May be misleading for low-earning companies.",
        "Threshold": "Below 15: Buy; 15-25: Hold; Above 25: Sell"
    },
    {
        "Metric": "P/B Ratio",
        "Current Value": f"{pb_ratio:.2f}" if isinstance(pb_ratio, (int, float)) else "N/A",
        "Pros": "Useful for asset-heavy industries.",
        "Cons": "Less relevant for tech or service companies.",
        "Threshold": "Below 1: Buy; 1-3: Hold; Above 3: Sell"
    },
    {
        "Metric": "D/E Ratio",
        "Current Value": f"{de_ratio:.2f}" if isinstance(de_ratio, (int, float)) else "N/A",
        "Pros": "Indicates financial leverage and risk.",
        "Cons": "Varies significantly by industry.",
        "Threshold": "Below 0.5: Buy; 0.5-1: Hold; Above 1: Sell"
    },
    {
        "Metric": "Free Cash Flow (FCF)",
        "Current Value": fcf_text,
        "Pros": "Indicates financial health and growth potential.",
        "Cons": "Can fluctuate significantly year to year.",
        "Threshold": "Positive: Buy; Negative: Sell"
    }
]

# Convert to DataFrame and display
recommendation_df = pd.DataFrame(recommendation_data)
st.table(recommendation_df)

    st.subheader("Recommendation")
    pe_ratio = info.get("trailingPE", "N/A")
    pb_ratio = info.get("priceToBook", "N/A")
    de_ratio = info.get("debtToEquity", "N/A")
    fcf = info.get("freeCashflow", "N/A")
    
    # Convert free cash flow to millions and format it
    fcf_text = f"{(fcf / 1e6):,.2f}M USD" if isinstance(fcf, (int, float)) else "N/A"
    
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
        return "N/A"  # Default case for undefined metrics

    # Prepare data for the table
    recommendation_data = [
        ["P/E Ratio", f"{pe_ratio:.2f}" if isinstance(pe_ratio, (int, float)) else "N/A", "Evaluates the stock's price relative to its earnings.", get_recommendation("P/E", pe_ratio)],
        ["P/B Ratio", f"{pb_ratio:.2f}" if isinstance(pb_ratio, (int, float)) else "N/A", "Compares the stock's market price to book value.", get_recommendation("P/B", pb_ratio)],
        ["D/E Ratio", f"{de_ratio:.2f}" if isinstance(de_ratio, (int, float)) else "N/A", "Measures financial leverage (debt vs equity).", get_recommendation("D/E", de_ratio)],
        ["Free Cash Flow (FCF)", fcf_text, "Cash generated after capital expenses.", get_recommendation("FCF", fcf)],
    ]

    # Create a DataFrame
    recommendation_df = pd.DataFrame(recommendation_data, columns=["Metric", "Current Value", "Explanation", "Recommendation"])
    
    # Display the Recommendation Table
    st.table(recommendation_df)

else:
    st.warning("Please enter a valid ticker symbol.")
