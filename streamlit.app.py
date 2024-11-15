import streamlit as st
import yfinance as yf
import pandas as pd

# Title and Introduction
st.title("Expanded Fundamental Analysis with Buy, Hold, Sell Recommendations")
st.markdown("""
This app provides a detailed fundamental analysis of a stock, including key financial metrics and overall recommendations (Buy, Hold, Sell) to help you make informed investment decisions.
""")

# User Input: Stock Ticker
ticker = st.text_input("Enter Stock Ticker (e.g., AAPL, MSFT):", value="AAPL")

# Fetch Stock Data
if ticker:
    stock = yf.Ticker(ticker)
    info = stock.info
    financials = stock.financials
    balance_sheet = stock.balance_sheet

    # ---- Fundamental Metrics ----
    st.header(f"Fundamental Analysis of {ticker}")
    
    # Market Cap in millions
    market_cap = info['marketCap'] / 1_000_000
    st.metric("Market Cap (in millions)", f"${market_cap:,.0f}M")

    # P/E Ratio
    pe_ratio = info.get('trailingPE', 'N/A')
    if pe_ratio != 'N/A':
        pe_recommendation = "Undervalued" if pe_ratio < 15 else "Overvalued" if pe_ratio > 25 else "Fairly Valued"
    else:
        pe_recommendation = "Data not available"
    
    st.subheader("P/E Ratio (Price-to-Earnings)")
    st.write(f"P/E Ratio: {pe_ratio}")
    st.write(f"Recommendation: {pe_recommendation}")
    st.markdown("""
    - **P/E Ratio** measures how much investors are willing to pay for each dollar of earnings.
    - **Undervalued**: A low P/E may indicate the stock is cheap relative to earnings.
    - **Overvalued**: A high P/E may suggest the stock is expensive.
    - **Fairly Valued**: A P/E between 15 and 25 is often considered a balanced value.
    """)

    # P/B Ratio
    pb_ratio = info.get('priceToBook', 'N/A')
    if pb_ratio != 'N/A':
        pb_recommendation = "Undervalued" if pb_ratio < 1 else "Overvalued" if pb_ratio > 3 else "Fairly Valued"
    else:
        pb_recommendation = "Data not available"

    st.subheader("P/B Ratio (Price-to-Book)")
    st.write(f"P/B Ratio: {pb_ratio}")
    st.write(f"Recommendation: {pb_recommendation}")
    st.markdown("""
    - **P/B Ratio** compares the market value of a company to its book value.
    - **Undervalued**: A P/B ratio less than 1 might indicate the stock is trading below its book value.
    - **Overvalued**: A high P/B ratio may suggest the stock is overpriced.
    - **Fairly Valued**: A P/B ratio between 1 and 3 is often considered normal.
    """)

    # Dividend Yield
    dividend_yield = info.get('dividendYield', 'N/A') * 100  # in percentage
    st.subheader("Dividend Yield")
    st.write(f"Dividend Yield: {dividend_yield:.2f}%")
    st.markdown("""
    - **Dividend Yield** shows how much a company pays out in dividends each year relative to its share price.
    - A **high dividend yield** may be attractive for income-seeking investors, but it can sometimes signal a risk of sustainability issues.
    - A **low or no dividend yield** is common in growth companies that reinvest earnings into expansion.
    """)

    # Return on Equity (ROE)
    roe = info.get('returnOnEquity', 'N/A')
    if roe != 'N/A':
        roe_recommendation = "Good" if roe > 15 else "Average" if roe > 5 else "Poor"
    else:
        roe_recommendation = "Data not available"
    
    st.subheader("Return on Equity (ROE)")
    st.write(f"ROE: {roe}%")
    st.write(f"Recommendation: {roe_recommendation}")
    st.markdown("""
    - **ROE** measures how efficiently a company is generating profits from its equity.
    - **Good**: An ROE above 15% suggests the company is using shareholder equity well.
    - **Average**: An ROE between 5% and 15% indicates average performance.
    - **Poor**: An ROE below 5% may suggest inefficiency.
    """)

    # Debt-to-Equity Ratio
    debt_to_equity = info.get('debtToEquity', 'N/A')
    if debt_to_equity != 'N/A':
        debt_recommendation = "Healthy" if debt_to_equity < 1 else "Risky" if debt_to_equity > 2 else "Moderate"
    else:
        debt_recommendation = "Data not available"
    
    st.subheader("Debt-to-Equity Ratio")
    st.write(f"Debt-to-Equity: {debt_to_equity}")
    st.write(f"Recommendation: {debt_recommendation}")
    st.markdown("""
    - **Debt-to-Equity Ratio** indicates how much debt a company has relative to equity.
    - **Healthy**: A low ratio (below 1) suggests the company is not over-leveraged.
    - **Risky**: A high ratio (above 2) suggests the company is highly leveraged and may face financial strain.
    - **Moderate**: A ratio between 1 and 2 is typical for most companies.
    """)

    # ---- Overall Recommendation (Buy, Hold, Sell) ----
    st.header("Overall Investment Recommendation")

    # Decision-making based on ratios:
    buy_count = 0
    hold_count = 0
    sell_count = 0

    # P/E Recommendation
    if pe_recommendation == "Undervalued":
        buy_count += 1
    elif pe_recommendation == "Overvalued":
        sell_count += 1
    else:
        hold_count += 1

    # P/B Recommendation
    if pb_recommendation == "Undervalued":
        buy_count += 1
    elif pb_recommendation == "Overvalued":
        sell_count += 1
    else:
        hold_count += 1

    # Dividend Yield (Considered "good" if greater than 3%)
    if dividend_yield > 3:
        buy_count += 1
    else:
        hold_count += 1

    # ROE Recommendation
    if roe != 'N/A':
        if roe > 15:
            buy_count += 1
        elif roe > 5:
            hold_count += 1
        else:
            sell_count += 1

    # Debt-to-Equity Recommendation
    if debt_to_equity != 'N/A':
        if debt_to_equity < 1:
            buy_count += 1
        elif debt_to_equity > 2:
            sell_count += 1
        else:
            hold_count += 1

    # Final Decision: Buy, Hold, or Sell
    if buy_count >= 3:
        recommendation = "Buy"
        recommendation_color = "green"
    elif sell_count >= 3:
        recommendation = "Sell"
        recommendation_color = "red"
    else:
        recommendation = "Hold"
        recommendation_color = "orange"

    st.markdown(f"### Overall Recommendation: **{recommendation}**")
    st.markdown(f"<h3 style='color:{recommendation_color};'>{recommendation}</h3>", unsafe_allow_html=True)

else:
    st.info("Please enter a stock ticker to begin analysis.")
