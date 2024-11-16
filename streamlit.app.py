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
    
    # Recommendation Section
    with st.expander("View Recommendation"):
        # Fetch key financial ratios
        pe_ratio = info.get("trailingPE", "N/A")
        pb_ratio = info.get("priceToBook", "N/A")
        de_ratio = info.get("debtToEquity", "N/A")
        fcf = info.get("freeCashflow", "N/A")
        peg_ratio = info.get("pegRatio", "N/A")
        
        # Convert free cash flow to millions
        if fcf != "N/A" and fcf is not None:
            fcf = fcf / 1e6
            fcf = round(fcf, 2)
        
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
            elif metric == "PEG":
                if value < 1:
                    return "Buy"
                elif 1 <= value <= 2:
                    return "Hold"
                else:
                    return "Sell"
            else:
                return "N/A"

        # Prepare data for the table
        recommendation_data = [
            ["P/E Ratio", pe_ratio, "Evaluates the stock's price relative to its earnings.", get_recommendation("P/E", pe_ratio)],
            ["P/B Ratio", pb_ratio, "Compares the stock's market price to book value.", get_recommendation("P/B", pb_ratio)],
            ["D/E Ratio", de_ratio, "Measures financial leverage (debt vs equity).", get_recommendation("D/E", de_ratio)],
            ["Free Cash Flow (FCF)", fcf, "Cash generated after capital expenses.", get_recommendation("FCF", fcf)],
            ["PEG Ratio", peg_ratio, "Price/Earnings-to-Growth Ratio.", get_recommendation("PEG", peg_ratio)],
        ]

        # Create a DataFrame
        recommendation_df = pd.DataFrame(recommendation_data, columns=["Metric", "Current Value", "Explanation", "Recommendation"])
        
        # Display the table
        st.subheader("Recommendation Table")
        st.table(recommendation_df)

else:
    st.warning("Please enter a valid ticker symbol.")
