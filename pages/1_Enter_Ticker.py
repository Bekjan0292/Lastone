import streamlit as st

st.title("Enter Stock Ticker")

if "ticker" not in st.session_state:
    st.session_state["ticker"] = ""

ticker = st.text_input("Enter stock ticker (e.g., AAPL, TSLA):", value=st.session_state["ticker"])
st.session_state["ticker"] = ticker

if ticker:
    st.success(f"Ticker '{ticker}' has been saved. Navigate to the other pages for analysis.")
else:
    st.info("Enter a ticker to begin.")
