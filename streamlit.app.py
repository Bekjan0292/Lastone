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
    
    # Key Statistics Section
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
    
    # Create a DataFrame for the statistics table
    stats_df = pd.DataFrame(stats_data, columns=["Metric", "Value", "Explanation"])
    st.table(stats_df)

else:
    st.warning("Please enter a valid ticker symbol.")
