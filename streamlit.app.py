import streamlit as st
import requests
import pandas as pd
import plotly.graph_objs as go
from PIL import Image

# Streamlit page settings
st.set_page_config(page_title="Interactive Stock Analysis", layout="wide", initial_sidebar_state="expanded")

# Enhanced CSS for a colorful theme
st.markdown("""
    <style>
        body {
            background-color: #f0f2f6;
            color: #333;
        }
        .block-container {
            padding: 2rem;
        }
        h1, h2, h3 {
            color: #2b5da4;
        }
        .stButton>button {
            background-color: #ff7f50;
            color: white;
            border-radius: 5px;
        }
        .stTable {
            background-color: #f7f9fc;
            color: #333;
        }
        .stSidebar {
            background-color: #eff2f5;
        }
        .css-1kcyg20 {
            background: url('https://images.unsplash.com/photo-1556741533-411cf82e4e2d') no-repeat center center fixed;
            background-size: cover;
        }
    </style>
""", unsafe_allow_html=True)

# Helper function to fetch stock data
@st.cache_data
def fetch_stock_data(ticker, modules="assetProfile,price"):
    url = f"https://query1.finance.yahoo.com/v10/finance/quoteSummary/{ticker}?modules={modules}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data["quoteSummary"]["result"][0]
    else:
        return None

# Interactive sidebar for user inputs
st.sidebar.header("Options")
ticker = st.sidebar.text_input("Stock Symbol", "AAPL")
buttonClicked = st.sidebar.button("Fetch Data")

# Main App
def main():
    st.title("Interactive Stock Analysis")

    if buttonClicked:
        st.subheader(f"Analyzing {ticker} Data")
        data = fetch_stock_data(ticker)

        if data:
            # Display stock profile information
            profile = data.get("assetProfile", {})
            price_data = data.get("price", {})

            st.write("### Company Profile")
            st.metric("Sector", profile.get("sector", "N/A"))
            st.metric("Industry", profile.get("industry", "N/A"))
            st.metric("Website", profile.get("website", "N/A"))
            st.metric("Market Cap", price_data.get("marketCap", {}).get("fmt", "N/A"))

            with st.expander("About Company"):
                st.write(profile.get("longBusinessSummary", "N/A"))

            # Display financial metrics in a colorful table
            st.write("### Financial Metrics")
            financial_metrics = {
                "P/E Ratio": price_data.get("trailingPE", {}).get("fmt", "N/A"),
                "P/B Ratio": price_data.get("priceToBook", {}).get("fmt", "N/A"),
                "EPS": price_data.get("epsCurrentYear", {}).get("fmt", "N/A"),
                "Dividend Yield": price_data.get("dividendYield", {}).get("fmt", "N/A"),
                "Profit Margin": profile.get("profitMargins", {}).get("fmt", "N/A"),
                "Current Ratio": profile.get("currentRatio", "N/A"),
                "ROE": profile.get("returnOnEquity", {}).get("fmt", "N/A"),
            }

            # Display metrics in a table format
            metric_df = pd.DataFrame(list(financial_metrics.items()), columns=["Metric", "Value"])
            st.table(metric_df)

            # Recommendations section
            st.write("### Investment Recommendation")
            recommendation = ""
            if financial_metrics["P/E Ratio"] != "N/A":
                pe_ratio = float(financial_metrics["P/E Ratio"])
                if pe_ratio < 15:
                    recommendation = "Buy - Low P/E ratio may indicate undervaluation."
                elif pe_ratio > 25:
                    recommendation = "Sell - High P/E ratio may indicate overvaluation."
                else:
                    recommendation = "Hold - Fairly valued."
            st.write(f"**Recommendation:** {recommendation}")

            # Interactive stock chart with Plotly
            st.write("### Stock Price Chart")
            stock_data = yf.download(ticker, period="1y")
            fig = go.Figure(data=[go.Candlestick(
                x=stock_data.index,
                open=stock_data["Open"],
                high=stock_data["High"],
                low=stock_data["Low"],
                close=stock_data["Close"],
                increasing_line_color="green",
                decreasing_line_color="red"
            )])
            fig.update_layout(title=f"{ticker} Stock Price (1 Year)", xaxis_title="Date", yaxis_title="Price (USD)")
            st.plotly_chart(fig)

            st.success("Data successfully loaded and displayed.")
        else:
            st.error("Failed to fetch data. Please check the ticker symbol and try again.")

if __name__ == "__main__":
    main()
