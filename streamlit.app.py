import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Page configuration
st.set_page_config(page_title="Financial Dashboard", layout="wide")

# Title and input
st.title("Financial Analysis Dashboard")

ticker = st.text_input("Enter Company Ticker (e.g., AAPL for Apple):", value="AAPL")
if ticker:
    try:
        # Fetching company data
        stock = yf.Ticker(ticker)

        # Header Section
        st.header(stock.info['longName'])
        st.subheader(stock.info['sector'] + " - " + stock.info['industry'])
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Market Cap:** ₹" + str(stock.info.get("marketCap", "N/A")))
            st.write("**Current Price:** ₹" + str(stock.info.get("previousClose", "N/A")))
            st.write("**High / Low:** ₹" + str(stock.info.get("fiftyTwoWeekHigh", "N/A")) + " / ₹" + str(stock.info.get("fiftyTwoWeekLow", "N/A")))
            st.write("**Stock P/E:** " + str(stock.info.get("trailingPE", "N/A")))
        
        with col2:
            st.write("**Dividend Yield:** " + str(stock.info.get("dividendYield", "N/A")) + "%")
            st.write("**Book Value:** ₹" + str(stock.info.get("bookValue", "N/A")))
            st.write("**ROE:** " + str(stock.info.get("returnOnEquity", "N/A")))
            st.write("**Face Value:** ₹" + str(stock.info.get("faceValue", "N/A")))

        # About and Key Points Section
        st.header("About")
        st.write(stock.info.get('longBusinessSummary', "No summary available."))
        
        # Price Chart with Time Range Selector
        st.header("Stock Price History")
        time_range = st.selectbox("Select Time Range:", ['1mo', '6mo', '1y', '5y', '10y'])
        hist = stock.history(period=time_range)
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(hist.index, hist['Close'], label="Close Price", color="blue")
        ax.set_title("Price History")
        ax.set_xlabel("Date")
        ax.set_ylabel("Price (₹)")
        ax.legend()
        st.pyplot(fig)

        # Financial Statements
        st.header("Financial Statements")

        with st.expander("Profit & Loss"):
            st.write(stock.financials if not stock.financials.empty else "No data available")

        with st.expander("Balance Sheet"):
            st.write(stock.balance_sheet if not stock.balance_sheet.empty else "No data available")

        with st.expander("Cash Flow"):
            st.write(stock.cashflow if not stock.cashflow.empty else "No data available")

        # Peer Comparison Section (Sample data, as peer data needs a different API source)
        st.header("Peer Comparison")
        st.write("Note: This section requires peer data which may not be directly available via yfinance.")
        # Sample static data
        sample_peers = pd.DataFrame({
            "Name": ["Apex Frozen Food", "Kings Infra", "Coastal Corporation", "Waterbase"],
            "P/E": [15.83, 35.03, 974.32, 16.92],
            "Market Cap (Rs. Cr.)": [719.66, 344.3, 302.04, 285.93],
            "Div Yield %": [0.87, 0.0, 0.53, 0.0]
        })
        st.table(sample_peers)

    except Exception as e:
        st.error(f"An error occurred: {e}")
