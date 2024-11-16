import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Установить параметры страницы
st.set_page_config(
    page_title="Stock Analyzer",
    page_icon="📊",
    layout="wide"
)

# Кеширование данных с помощью @st.cache_data
@st.cache_data
def get_stock_data(ticker):
    stock = yf.Ticker(ticker)
    return stock.info, stock.financials.T, stock.history(period="5y")

# Инициализация session_state для тикера и текущей страницы
if "ticker" not in st.session_state:
    st.session_state["ticker"] = ""
if "page" not in st.session_state:
    st.session_state["page"] = "Main"
if "stock_data" not in st.session_state:
    st.session_state["stock_data"] = None

# Главная страница
def main_page():
    st.title("Stock Analyzer")
    st.write("Добро пожаловать! Здесь вы можете анализировать акции как фундаментально, так и технически.")

    # Поле для ввода тикера
    ticker = st.text_input("Введите тикер акции (например, AAPL, TSLA):", value=st.session_state["ticker"])
    st.session_state["ticker"] = ticker

    # Кнопки для перехода
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Перейти к фундаментальному анализу") and ticker:
            # Загружаем и сохраняем данные в session_state
            st.session_state["stock_data"] = get_stock_data(ticker)
            st.session_state["page"] = "Fundamental"
    with col2:
        if st.button("Перейти к техническому анализу") and ticker:
            st.session_state["stock_data"] = get_stock_data(ticker)
            st.session_state["page"] = "Technical"

# Страница фундаментального анализа
def fundamental_analysis_page():
    st.title("Фундаментальный анализ")

    # Проверка наличия данных
    if not st.session_state["stock_data"]:
        st.warning("Пожалуйста, вернитесь на главную страницу и введите тикер.")
        return

    # Получение данных из session_state
    info, financials, history = st.session_state["stock_data"]

    # Информация о компании
    st.subheader(f"Компания: {info.get('longName', 'Неизвестно')} ({st.session_state['ticker']})")
    st.write(f"**Сектор:** {info.get('sector', 'N/A')} | **Отрасль:** {info.get('industry', 'N/A')}")

    # Ключевые метрики
    st.subheader("Ключевые финансовые метрики")
    metrics = {
        "Рыночная капитализация": f"${info.get('marketCap', 0):,}",
        "P/E (TTM)": info.get('forwardPE', 'N/A'),
        "Дивидендная доходность": f"{info.get('dividendYield', 0) * 100:.2f}%",
        "52-недельный максимум": f"${info.get('fiftyTwoWeekHigh', 'N/A')}",
        "52-недельный минимум": f"${info.get('fiftyTwoWeekLow', 'N/A')}"
    }
    metrics_df = pd.DataFrame(metrics.items(), columns=["Метрика", "Значение"])

    # Устранение ошибок Arrow, конвертация в строки
    metrics_df["Значение"] = metrics_df["Значение"].astype(str)
    st.table(metrics_df)

    # График "Выручка и чистая прибыль"
    st.subheader("Выручка и чистая прибыль (интерактивный график)")
    try:
        financials = financials.rename(columns={"Total Revenue": "Выручка", "Net Income": "Чистая прибыль"})
        financials_chart = financials[["Выручка", "Чистая прибыль"]].reset_index()
        financials_chart = financials_chart.melt(id_vars="index", var_name="Метрика", value_name="Сумма")
        fig = px.line(
            financials_chart,
            x="index",
            y="Сумма",
            color="Метрика",
            title="Тренды выручки и чистой прибыли",
            labels={"index": "Год", "Сумма": "Сумма (USD)"}
        )
        st.plotly_chart(fig)
    except Exception:
        st.warning("Не удалось загрузить данные по выручке и прибыли.")

    # Рекомендация
    st.subheader("Рекомендация")
    recommendation = "Держать"
    pe = info.get("forwardPE", None)
    if pe:
        if pe < 15:
            recommendation = "Покупать"
        elif pe > 25:
            recommendation = "Продавать"

    # График-индикатор
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=pe if pe else 20,
        title={"text": f"P/E Ratio ({recommendation})"},
        gauge={
            "axis": {"range": [0, 40]},
            "bar": {"color": "green" if recommendation == "Покупать" else "red" if recommendation == "Продавать" else "yellow"}
        }
    ))
    st.plotly_chart(fig)

    # Кнопка "Назад"
    if st.button("Назад на главную страницу"):
        st.session_state["page"] = "Main"

# Страница технического анализа (плейсхолдер)
def technical_analysis_page():
    st.title("Технический анализ")
    st.write("Здесь будет реализован технический анализ.")

    # Кнопка "Назад"
    if st.button("Назад на главную страницу"):
        st.session_state["page"] = "Main"

# Навигация между страницами
if st.session_state["page"] == "Main":
    main_page()
elif st.session_state["page"] == "Fundamental":
    fundamental_analysis_page()
elif st.session_state["page"] == "Technical":
    technical_analysis_page()
    
