import streamlit as st
import os

# Настройки страницы
st.set_page_config(
    page_title="Stock Analysis",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Проверка наличия фонового изображения
background_path = "background.jpg"
if not os.path.exists(background_path):
    st.warning("Background image not found! Please ensure 'background.jpg' is in the app directory.")

# CSS для добавления фонового изображения
st.markdown(f"""
    <style>
        body {{
            margin: 0;
            padding: 0;
            background-image: url('{background_path}');
            background-size: cover;
            background-attachment: fixed;
            background-position: center;
            font-family: Arial, sans-serif;
            color: black;
        }}
        .block-container {{
            padding: 2rem;
            background: none; /* Удаляем фон для блока */
        }}
        h1, h2, h3 {{
            color: black;
        }}
        label, .stRadio label {{
            color: black;
        }}
        .stTextInput>div>label {{
            color: black;
        }}
        .stButton>button {{
            background-color: #1b1b1b;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 0.5rem 1rem;
            font-size: 1rem;
        }}
        .stButton>button:hover {{
            background-color: #00c853;
        }}
    </style>
""", unsafe_allow_html=True)

# Заголовок сайта
st.title("Stock Analysis")

# Опция выбора компании
st.subheader("Step 1: Choose a Company")
company = st.text_input("Enter the company symbol (e.g., AAPL for Apple, MSFT for Microsoft):")

# Опции выбора типа анализа
st.subheader("Step 2: Select Type of Analysis")
analysis_type = st.radio(
    "Choose the type of analysis:",
    ("Fundamental Analysis", "Technical Analysis")
)

# Объяснение выбранного анализа
st.subheader("What is this Analysis?")
if analysis_type == "Fundamental Analysis":
    st.markdown("""
        **Fundamental Analysis** is a method of evaluating a company's intrinsic value by analyzing related economic, financial, and qualitative and quantitative factors. 
        It looks at revenue, earnings, future growth, return on equity, profit margins, and other data to determine a company’s underlying value and potential for growth.
    """, unsafe_allow_html=True)
elif analysis_type == "Technical Analysis":
    st.markdown("""
        **Technical Analysis** is a trading discipline that evaluates investments and identifies trading opportunities by analyzing statistical trends gathered from trading activity. 
        It focuses on patterns in price movements, volume, and other charting tools to forecast future price movements.
    """, unsafe_allow_html=True)

# Интерактивная кнопка для перехода к анализу
if company:
    st.write(f"Selected Company: **{company.upper()}**")
    if st.button("Proceed with Analysis"):
        st.success(f"Starting {analysis_type.lower()} for {company.upper()}...")
if analysis_type == "Fundamental Analysis" and data:
    display_fundamental_analysis(data)
    import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# Функция для получения данных через yfinance
@st.cache_data
def fetch_company_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        return stock.info
    except Exception as e:
        st.error(f"Error fetching data for {ticker}: {e}")
        return None

# Функция для добавления подсказок
def add_tooltip(text, tooltip):
    return f"<span title='{tooltip}' style='text-decoration: underline dotted;'>{text}</span>"

# Отображение фундаментального анализа
def display_fundamental_analysis(data):
    st.header("Fundamental Analysis")
    
    # Общая информация
    st.subheader("Company Overview")
    st.write(f"**Name:** {data.get('shortName', 'N/A')}")
    st.write(f"**Sector:** {data.get('sector', 'N/A')}")
    st.write(f"**Industry:** {data.get('industry', 'N/A')}")
    st.write(f"**Website:** [Visit Website]({data.get('website', 'N/A')})")
    st.write(f"**Description:** {data.get('longBusinessSummary', 'N/A')}")

    # Финансовые показатели с подсказками
    st.subheader("Financial Performance")
    st.write("Analyzing the company's revenue, net income, and profit margin provides insights into its financial health.")

    financial_performance = {
        add_tooltip("Revenue (TTM)", "Total revenue over the trailing twelve months."): data.get("totalRevenue", "N/A"),
        add_tooltip("Net Income (TTM)", "Net income over the trailing twelve months."): data.get("netIncomeToCommon", "N/A"),
        add_tooltip("Profit Margin", "Net income divided by revenue, showing profitability."): data.get("profitMargins", "N/A"),
        add_tooltip("Operating Margin", "Operating income divided by revenue, showing operational efficiency."): data.get("operatingMargins", "N/A")
    }

    performance_df = pd.DataFrame(list(financial_performance.items()), columns=["Metric", "Value"])
    st.write(performance_df.to_html(escape=False, index=False), unsafe_allow_html=True)

    # Показатели роста с подсказками
    st.subheader("Growth Metrics")
    st.write("Growth metrics provide insights into how the company has grown over time in terms of revenue and earnings.")

    growth_metrics = {
        add_tooltip("Revenue Growth (Quarterly YoY)", "Growth rate of revenue compared to the same quarter last year."): data.get("revenueGrowth", "N/A"),
        add_tooltip("Earnings Growth (Quarterly YoY)", "Growth rate of earnings compared to the same quarter last year."): data.get("earningsGrowth", "N/A")
    }

    growth_df = pd.DataFrame(list(growth_metrics.items()), columns=["Metric", "Value"])
    st.write(growth_df.to_html(escape=False, index=False), unsafe_allow_html=True)

    # Долговая нагрузка
    st.subheader("Debt and Leverage")
    st.write("Evaluating the company's leverage provides a view of its financial risk.")

    debt_ratios = {
        add_tooltip("Debt to Equity Ratio", "Total liabilities divided by shareholder equity. Lower is generally better."): data.get("debtToEquity", "N/A"),
        add_tooltip("Current Ratio", "Current assets divided by current liabilities. Higher indicates better short-term liquidity."): data.get("currentRatio", "N/A"),
        add_tooltip("Quick Ratio", "Current assets minus inventory, divided by current liabilities. A stricter measure of liquidity."): data.get("quickRatio", "N/A")
    }

    debt_df = pd.DataFrame(list(debt_ratios.items()), columns=["Metric", "Value"])
    st.write(debt_df.to_html(escape=False, index=False), unsafe_allow_html=True)

    # Дивиденды
    st.subheader("Dividend Analysis")
    st.write("Dividends are a reflection of a company's profitability and its ability to return value to shareholders.")

    dividend_data = {
        add_tooltip("Dividend Yield", "Annual dividend payments as a percentage of the stock price."): data.get("dividendYield", "N/A"),
        add_tooltip("Payout Ratio", "Proportion of earnings paid out as dividends."): data.get("payoutRatio", "N/A"),
        add_tooltip("Five-Year Avg Dividend Yield", "Average dividend yield over the past five years."): data.get("fiveYearAvgDividendYield", "N/A")
    }

    dividend_df = pd.DataFrame(list(dividend_data.items()), columns=["Metric", "Value"])
    st.write(dividend_df.to_html(escape=False, index=False), unsafe_allow_html=True)

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
