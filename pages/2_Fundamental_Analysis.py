import streamlit as st
import yfinance as yf

st.title("Fundamental Analysis")

if "ticker" not in st.session_state or not st.session_state["ticker"]:
    st.warning("Please enter a stock ticker on the 'Enter Ticker' page first.")
else:
    ticker = st.session_state["ticker"]

    stock = yf.Ticker(ticker)
    info = stock.info

    st.subheader(f"{info.get('longName', 'Unknown Company')} ({ticker})")

    st.markdown(f"""
    **Sector**: {info.get('sector', 'N/A')}  
    **Industry**: {info.get('industry', 'N/A')}  
    **Market Cap**: ${info.get('marketCap', 0):,}  
    **PE Ratio (TTM)**: {info.get('forwardPE', 'N/A')}  
    **Dividend Yield**: {info.get('dividendYield', 0) * 100:.2f}%  
    **52-Week High**: ${info.get('fiftyTwoWeekHigh', 'N/A')}  
    **52-Week Low**: ${info.get('fiftyTwoWeekLow', 'N/A')}  
    """)
