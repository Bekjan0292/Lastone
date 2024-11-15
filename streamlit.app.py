import streamlit as st

# Настройки страницы
st.set_page_config(
    page_title="Stock Analysis Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Темный фон и стиль через CSS
st.markdown("""
    <style>
        body {
            background-image: url('https://source.unsplash.com/1920x1080/?finance,stock');
            background-size: cover;
            background-attachment: fixed;
            color: #e0e0e0;
            font-family: Arial, sans-serif;
        }
        .block-container {
            background: rgba(0, 0, 0, 0.8);
            padding: 2rem;
            border-radius: 10px;
        }
        h1, h2, h3 {
            color: #00c853;
        }
        .stButton>button {
            background-color: #1b1b1b;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 0.5rem 1rem;
            font-size: 1rem;
        }
        .stButton>button:hover {
            background-color: #00c853;
        }
    </style>
""", unsafe_allow_html=True)

# Заголовок сайта
st.title("Stock Analysis Dashboard")

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
    st.write("""
        **Fundamental Analysis** is a method of evaluating a company's intrinsic value by analyzing related economic, financial, and qualitative and quantitative factors. 
        It looks at revenue, earnings, future growth, return on equity, profit margins, and other data to determine a company’s underlying value and potential for growth.
    """)
elif analysis_type == "Technical Analysis":
    st.write("""
        **Technical Analysis** is a trading discipline that evaluates investments and identifies trading opportunities by analyzing statistical trends gathered from trading activity. 
        It focuses on patterns in price movements, volume, and other charting tools to forecast future price movements.
    """)

# Интерактивная кнопка для перехода к анализу
if company:
    st.write(f"Selected Company: **{company.upper()}**")
    if st.button("Proceed with Analysis"):
        st.success(f"Starting {analysis_type.lower()} for {company.upper()}...")
