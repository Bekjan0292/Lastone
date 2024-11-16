def fundamental_analysis_page():
    st.title("Fundamental Analysis")

    if not st.session_state["stock_data"]:
        st.warning("Please go back to the main page and enter a stock ticker.")
        return

    # Retrieve data from session_state
    info, financials, history = st.session_state["stock_data"]

    # Company Information
    st.subheader(f"Company: {info.get('longName', 'Unknown')} ({st.session_state['ticker']})")
    st.write(f"**Sector:** {info.get('sector', 'N/A')} | **Industry:** {info.get('industry', 'N/A')}")

    # Valuation Metrics
    st.subheader("Valuation Metrics")
    valuation_metrics = {
        "P/E Ratio": info.get('forwardPE', 'N/A'),
        "P/S Ratio": info.get('priceToSalesTrailing12Months', 'N/A'),
        "P/B Ratio": info.get('priceToBook', 'N/A'),
    }
    valuation_df = pd.DataFrame(valuation_metrics.items(), columns=["Metric", "Value"])
    valuation_df["Value"] = valuation_df["Value"].astype(str)
    st.table(valuation_df)

    # Profitability Metrics
    st.subheader("Profitability Metrics")
    profitability_metrics = {
        "Return on Equity (ROE)": f"{info.get('returnOnEquity', 0) * 100:.2f}%",
        "Return on Assets (ROA)": f"{info.get('returnOnAssets', 0) * 100:.2f}%",
    }
    profitability_df = pd.DataFrame(profitability_metrics.items(), columns=["Metric", "Value"])
    profitability_df["Value"] = profitability_df["Value"].astype(str)
    st.table(profitability_df)

    # Financial Health
    st.subheader("Financial Health")
    financial_health_metrics = {
        "Debt-to-Equity Ratio": info.get('debtToEquity', 'N/A'),
        "Current Ratio": info.get('currentRatio', 'N/A'),
        "Quick Ratio": info.get('quickRatio', 'N/A'),
    }
    financial_health_df = pd.DataFrame(financial_health_metrics.items(), columns=["Metric", "Value"])
    financial_health_df["Value"] = financial_health_df["Value"].astype(str)
    st.table(financial_health_df)

    # Growth Metrics
    st.subheader("Growth Metrics")
    growth_metrics = {
        "Earnings Per Share (EPS)": info.get('trailingEps', 'N/A'),
        "Revenue Growth (YoY)": f"{info.get('revenueGrowth', 0) * 100:.2f}%",
    }
    growth_df = pd.DataFrame(growth_metrics.items(), columns=["Metric", "Value"])
    growth_df["Value"] = growth_df["Value"].astype(str)
    st.table(growth_df)

    # Dividends
    st.subheader("Dividends")
    dividend_metrics = {
        "Dividend Yield": f"{info.get('dividendYield', 0) * 100:.2f}%",
        "Dividend Payout Ratio": f"{info.get('payoutRatio', 0) * 100:.2f}%",
    }
    dividend_df = pd.DataFrame(dividend_metrics.items(), columns=["Metric", "Value"])
    dividend_df["Value"] = dividend_df["Value"].astype(str)
    st.table(dividend_df)

    # Risk Indicators
    st.subheader("Risk Indicators")
    risk_metrics = {
        "Beta": info.get('beta', 'N/A'),
        "Interest Coverage Ratio": info.get('interestCoverage', 'N/A'),
    }
    risk_df = pd.DataFrame(risk_metrics.items(), columns=["Metric", "Value"])
    risk_df["Value"] = risk_df["Value"].astype(str)
    st.table(risk_df)

    # Back button
    if st.button("Back to Main Page"):
        st.session_state["page"] = "Main"
    
