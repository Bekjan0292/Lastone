import streamlit as st
import yfinance as yf
import pandas as pd

# Page settings
st.set_page_config(
    page_title="Stock Analysis",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cache the function to reduce API calls
@st.cache_data
def fetch_selected_company_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        return {
            "shortName": stock.info.get("shortName", "N/A"),
            "sector": stock.info.get("sector", "N/A"),
            "industry": stock.info.get("industry", "N/A"),
            "website": stock.info.get("website", "N/A"),
            "longBusinessSummary": stock.info.get("longBusinessSummary", "N/A"),
            "totalRevenue": stock.info.get("totalRevenue", "N/A"),
            "netIncomeToCommon": stock.info.get("netIncomeToCommon", "N/A"),
            "profitMargins": stock.info.get("profitMargins", "N/A"),
            "revenueGrowth": stock.info.get("revenueGrowth", "N/A"),
            "earningsGrowth": stock.info.get("earningsGrowth", "N/A"),
            "debtToEquity": stock.info.get("debtToEquity", "N/A"),
            "currentRatio": stock.info.get("currentRatio", "N/A"),
            "quickRatio": stock.info.get("quickRatio", "N/A"),
        }
    except Exception as e:
        st.error(f"Error fetching data for {ticker}: {e}")
        return None

def display_fundamental_analysis(data):
    st.header("Fundamental Analysis")
    st.subheader("Basic Information")
    st.write(f"**Name:** {data['shortName']}")
    st.write(f"**Sector:** {data['sector']}")
    st.write(f"**Industry:** {data['industry']}")
    st.write(f"**Website:** [Visit Website]({data['website']})")

    st.subheader("Company Description")
    st.write(data["longBusinessSummary"])

    st.subheader("Financial Metrics")
    financial_data = {
        "Total Revenue": data["totalRevenue"],
        "Net Income": data["netIncomeToCommon"],
        "Profit Margin": data["profitMargins"],
        "Revenue Growth (YoY)": data["revenueGrowth"],
        "Earnings Growth (YoY)": data["earningsGrowth"]
    }
    st.table(pd.DataFrame(financial_data.items(), columns=["Metric", "Value"]))

    st.subheader("Debt and Leverage Metrics")
    debt_data = {
        "Debt to Equity Ratio": data["debtToEquity"],
        "Current Ratio": data["currentRatio"],
        "Quick Ratio": data["quickRatio"]
    }
    st.table(pd.DataFrame(debt_data.items(), columns=["Metric", "Value"]))

# Page navigation logic
if "page" not in st.session_state:
    st.session_state.page = "Home"

if st.session_state.page == "Home":
    st.title("Welcome to Stock Analysis")
    st.subheader("Step 1: Choose a Company")
    company = st.text_input("Enter the company symbol (e.g., AAPL for Apple):")

    st.subheader("Step 2: Select Type of Analysis")
    analysis_type = st.radio(
        "Choose the type of analysis:",
        ("Fundamental Analysis", "Technical Analysis")
    )

    st.subheader("What is this Analysis?")
    if analysis_type == "Fundamental Analysis":
        st.markdown("""
            **Fundamental Analysis** evaluates a company's intrinsic value by analyzing economic, financial, and qualitative factors.
        """)
    elif analysis_type == "Technical Analysis":
        st.markdown("""
            **Technical Analysis** analyzes statistical trends from trading activity to identify trading opportunities.
        """)

    if company and analysis_type == "Fundamental Analysis":
        if st.button("Go to Fundamental Analysis"):
            with st.spinner("Fetching company data..."):
                data = fetch_selected_company_data(company)
                if data:
                    st.session_state.page = "Fundamental Analysis"
                    st.session_state.company_data = data
                else:
                    st.error("Failed to fetch company data. Please try again.")

elif st.session_state.page == "Fundamental Analysis":
    st.title("Fundamental Analysis")
    data = st.session_state.get("company_data", None)

    if data:
        display_fundamental_analysis(data)
    else:
        st.error("No data available. Please return to the Home page.")
    if st.button("Back to Home"):
        st.session_state.page = "Home"
