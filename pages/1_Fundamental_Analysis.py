import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd

# Page Config
st.set_page_config(page_title="Stock Fundamental Analysis", layout="wide")

# Main Input Section
st.title("Stock Fundamental Analysis")
ticker = st.text_input("Enter Stock Ticker:", value="AAPL")
go_button = st.button("Go")

# Fetch Data when "Go" is clicked
if go_button and ticker:
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
    
