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
    
    # Key statistics in compact table format with tooltips
    st.subheader("Key Statistics")
    stats_data = [
        [
            f'<span title="The current trading price of the stock.">Current Price</span>',
            f"${info['currentPrice']:.2f}",
            f'<span title="The total value of the company based on its stock price and shares outstanding.">Market Cap</span>',
            f"${info['marketCap'] / 1e9:,.2f}B"
        ],
        [
            f'<span title="The range of the stock price over the last 52 weeks.">52W Range</span>',
            f"{info['fiftyTwoWeekLow']:.2f} - {info['fiftyTwoWeekHigh']:.2f}",
            f'<span title="The last recorded closing price of the stock.">Previous Close</span>',
            f"${info['previousClose']:.2f}"
        ],
        [
            f'<span title="The stock price at the start of the trading session.">Open</span>',
            f"${info['open']:.2f}",
            f'<span title="The lowest and highest price during today\'s trading session.">Day\'s Range</span>',
            f"{info['dayLow']:.2f} - {info['dayHigh']:.2f}"
        ],
        [
            f'<span title="A measure of the stock\'s volatility compared to the overall market.">Beta</span>',
            f"{info['beta']:.2f}",
            f'<span title="The price-to-earnings ratio, showing the price relative to earnings per share.">P/E Ratio</span>',
            f"{info.get('trailingPE', 'N/A'):.2f}" if info.get('trailingPE') else "N/A"
        ],
        [
            f'<span title="The price-to-book ratio, showing the price relative to book value per share.">P/B Ratio</span>',
            f"{info.get('priceToBook', 'N/A'):.2f}" if info.get('priceToBook') else "N/A",
            f'<span title="Earnings per share, showing profit allocated to each outstanding share.">EPS</span>',
            f"{info.get('trailingEps', 'N/A'):.2f}" if info.get('trailingEps') else "N/A"
        ]
    ]
    
    # Convert the data into a DataFrame with HTML tooltips
    stats_df = pd.DataFrame(stats_data, columns=["Metric 1", "Value 1", "Metric 2", "Value 2"])
    
    # Render the table with tooltips
    st.markdown(
        stats_df.to_html(escape=False, index=False, border=0),
        unsafe_allow_html=True
    )
    
    # Financial metrics
    st.subheader("Financial Analysis")
    with st.expander("Income Statement"):
        st.write("Revenue, Net Income, etc.")
    with st.expander("Balance Sheet"):
        st.write("Total Assets, Liabilities, etc.")
    with st.expander("Cash Flow"):
        st.write("Operating Cash Flow, etc.")
else:
    st.warning("Please enter a valid ticker symbol.")
