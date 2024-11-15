import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# Настройки страницы
st.set_page_config(
    page_title="Stock Analysis",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Функция для получения данных через yfinance
@st.cache_data
def fetch_company_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        return stock.info
    except Exception as e:
        st.error(f"Error fetching data for {ticker}: {e}")
        return None

# Функция для отображения фундаментального анализа
def display_fundamental_analysis(data):
    st.header("Fundamental Analysis")
    
    # Общая информация
    st.subheader("Company Overview")
    st.write(f"**Name:** {data.get('shortName', 'N/A')}")
    st.write(f"**Sector:** {data.get('sector', 'N/A')}")
    st.write(f"**Industry:** {data.get('industry', 'N/A')}")
    st.write(f"**Website:** [Visit Website]({data.get('website', 'N/A')})")
    st.write(f"**Description:** {data.get('longBusinessSummary', 'N/A')}")

    # Финансовые показатели
    st.subheader("Financial Performance")
    financial_performance = {
        "Revenue (TTM)": data.get("totalRevenue", "N/A"),
        "Net Income (TTM)": data.get("netIncomeToCommon", "N/A"),
        "Profit Margin": data.get("profitMargins", "N/A"),
        "Operating Margin": data.get("operatingMargins", "N/A")
    }
    financial_df = pd.DataFrame(list(financial_performance.items()), columns=["Metric", "Value"])
    st.table(financial_df)

    # Показатели роста
    st.subheader("Growth Metrics")
    growth_metrics = {
        "Revenue Growth (Quarterly YoY)": data.get("revenueGrowth", "N/A"),
        "Earnings Growth (Quarterly YoY)": data.get("earningsGrowth", "N/A")
    }
    growth_df = pd.DataFrame(list(growth_metrics.items()), columns=["Metric", "Value"])
    st.table(growth_df)

    # Долговая нагрузка
    st.subheader("Debt and Leverage")
    debt_ratios = {
        "Debt to Equity Ratio": data.get("debtToEquity", "N/A"),
        "Current Ratio": data.get("currentRatio", "N/A"),
        "Quick Ratio": data.get("quickRatio", "N/A")
    }
    debt_df = pd.DataFrame(list(debt_ratios.items()), columns=["Metric", "Value"])
    st.table(debt_df)

    # Графическое представление
    st.subheader("Visual Representation of Financial Ratios")
    financial_ratios = {
        "P/E Ratio": data.get("trailingPE", 0),
        "P/B Ratio": data.get("priceToBook", 0),
        "Return on Equity (ROE)": data.get("returnOnEquity", 0),
        "Profit Margin": data.get("profitMargins", 0)
    }
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=list(financial_ratios.keys()),
        y=list(financial_ratios.values()),
        marker_color='indigo'
    ))
    fig.update_layout(
        title="Key Financial Ratios",
        xaxis_title="Metrics",
        yaxis_title="Values",
        template="plotly_dark"
    )
    st.plotly_chart(fig)

# Основная логика страниц
menu = st.sidebar.radio("Navigate", ["Home", "Fundamental Analysis"])

if menu == "Home":
    # Стартовая страница
    st.title("Welcome to Stock Analysis")
    st.subheader("Step 1: Choose a Company")
    company = st.text_input("Enter the company symbol (e.g., AAPL for Apple, MSFT for Microsoft):")

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

    if company and st.button("Go to Fundamental Analysis"):
        st.session_state["company"] = company
        st.session_state["navigate"] = "Fundamental Analysis"

elif menu == "Fundamental Analysis":
    st.title("Fundamental Analysis")

    # Получение символа компании из состояния
    company = st.session_state.get("company", None)

    if company:
        data = fetch_company_data(company)
        if data:
            display_fundamental_analysis(data)
        else:
            st.error(f"Failed to load data for {company}. Please return to the Home page.")
    else:
        st.error("No company selected. Please return to the Home page.")
