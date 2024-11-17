import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd

def perform_analysis(ticker, analysis_type):
    if analysis_type == "Technical Analysis":
        st.subheader(f"Technical Analysis for {ticker}")
        st.write("Performing technical analysis...")
        # Add your technical analysis logic here
    
    elif analysis_type == "Fundamental Analysis":
        st.subheader (f"{info['longName']} ({ticker.upper()})")
        stock = yf.Ticker(ticker)
        info = stock.info
        historical = stock.history(period="1y")

        # Company Information
        st.title(f"{info.get('longName', ticker.upper())}")
        with st.expander("About the Company"):
            st.write(info.get("longBusinessSummary", "Company information is not available."))

        st.write(f"**Industry:** {info.get('industry', 'N/A')}")
        st.write(f"**Country:** {info.get('country', 'N/A')}")
        st.markdown(f"[**Website**]({info.get('website', 'N/A')})", unsafe_allow_html=True)

        # Candlestick Chart
        fig = go.Figure()
        fig.add_trace(
            go.Candlestick(
                x=historical.index,
                open=historical['Open'],
                high=historical['High'],
                low=historical['Low'],
                close=historical['Close']
            )
        )
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Price (USD)",
            template="plotly_white"
        )
        st.plotly_chart(fig)

        # Key Statistics
        st.subheader("Key Statistics")
        stats_data = [
            ["Current Price", f"${info.get('currentPrice', 'N/A'):.2f}"],
            ["Market Cap", f"${info.get('marketCap', 'N/A') / 1e9:.2f}B"],
            ["52W Range", f"{info.get('fiftyTwoWeekLow', 'N/A'):.2f} - {info.get('fiftyTwoWeekHigh', 'N/A'):.2f}"],
            ["Beta", f"{info.get('beta', 'N/A'):.2f}"],
            ["P/E Ratio", f"{info.get('trailingPE', 'N/A'):.2f}" if info.get("trailingPE") else "N/A"],
        ]
        stats_df = pd.DataFrame(stats_data, columns=["Metric", "Value"])
        st.table(stats_df)

        # Balance Sheet and Income Statement
        if st.button("View Income Statement"):
            st.write("Income statement logic goes here (extract from provided code).")
        if st.button("View Balance Sheet"):
            st.write("Balance sheet logic goes here (extract from provided code).")

        # Recommendation
        st.subheader("Recommendation")
        recommendations = [
            ["Metric", "Current Value", "Recommendation"],
            ["P/E Ratio", info.get('trailingPE', "N/A"), "Buy" if info.get('trailingPE', 0) < 15 else "Hold"]
        ]
        st.table(pd.DataFrame(recommendations, columns=["Metric", "Value", "Recommendation"]))
