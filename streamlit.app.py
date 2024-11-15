import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Настройка страницы
st.set_page_config(page_title="Финансовый анализ компании", layout="wide")

# Заголовок
st.title("Финансовый анализ компании")

# Ввод тикера компании
ticker = st.text_input("Введите тикер компании (например, AAPL для Apple):", value="AAPL")

if ticker:
    try:
        # Получение данных компании
        stock = yf.Ticker(ticker)
        
        # Основная информация о компании
        st.header("Основная информация")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Название компании:** {stock.info.get('longName', 'N/A')}")
            st.write(f"**Сектор:** {stock.info.get('sector', 'N/A')}")
            st.write(f"**Отрасль:** {stock.info.get('industry', 'N/A')}")
            st.write(f"**Рыночная капитализация:** {stock.info.get('marketCap', 'N/A')}")
        with col2:
            st.write(f"**Страна:** {stock.info.get('country', 'N/A')}")
            st.write(f"**P/E (Price to Earnings):** {stock.info.get('trailingPE', 'N/A')}")
            st.write(f"**Дивидендная доходность:** {stock.info.get('dividendYield', 'N/A')}")

        # История цен акций
        st.header("График акций")
        hist = stock.history(period="5y")
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(hist.index, hist["Close"], label="Цена закрытия")
        ax.set_title("График изменения цен акций")
        ax.set_xlabel("Дата")
        ax.set_ylabel("Цена (USD)")
        ax.legend()
        st.pyplot(fig)

        # Финансовые показатели
        st.header("Финансовые показатели")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.subheader("Доходы")
            st.write(stock.financials.loc["Total Revenue"].T if not stock.financials.empty else "Нет данных")
        with col2:
            st.subheader("Прибыль")
            st.write(stock.financials.loc["Net Income"].T if not stock.financials.empty else "Нет данных")
        with col3:
            st.subheader("Операционная прибыль")
            st.write(stock.financials.loc["Operating Income"].T if not stock.financials.empty else "Нет данных")
        
        # Балансовый отчет
        st.header("Балансовый отчет")
        st.write(stock.balance_sheet if not stock.balance_sheet.empty else "Данные недоступны")

        # Отчет о движении денежных средств
        st.header("Движение денежных средств")
        st.write(stock.cashflow if not stock.cashflow.empty else "Данные недоступны")

        # График распределения доходов
        st.header("Распределение доходов")
        if not stock.financials.empty:
            revenue = stock.financials.loc["Total Revenue"]
            if not revenue.empty:
                fig, ax = plt.subplots(figsize=(8, 4))
                ax.bar(revenue.index, revenue.values, color='blue')
                ax.set_title("График доходов")
                ax.set_ylabel("Доходы (в миллионах)")
                st.pyplot(fig)
            else:
                st.write("Нет данных для построения графика.")
        else:
            st.write("Финансовые данные недоступны.")

    except Exception as e:
        st.error(f"Ошибка: {e}")
