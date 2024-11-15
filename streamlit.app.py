import streamlit as st
import yfinance as yf
import pandas as pd

# Настройка интерфейса
st.title("Анализ компаний с использованием данных YFinance")

# Ввод тикера компании
ticker = st.text_input("Введите тикер компании (например, AAPL для Apple):", value="AAPL")

if ticker:
    try:
        # Получение данных компании
        stock = yf.Ticker(ticker)

        # Основная информация о компании
        st.header("Основная информация")
        st.write(f"**Название компании:** {stock.info.get('longName', 'N/A')}")
        st.write(f"**Описание:** {stock.info.get('longBusinessSummary', 'N/A')}")
        st.write(f"**Сектор:** {stock.info.get('sector', 'N/A')}")
        st.write(f"**Отрасль:** {stock.info.get('industry', 'N/A')}")
        st.write(f"**Страна:** {stock.info.get('country', 'N/A')}")

        # Ключевые показатели
        st.header("Ключевые показатели")
        st.write(f"**Рыночная капитализация:** {stock.info.get('marketCap', 'N/A')}")
        st.write(f"**P/E (Price to Earnings):** {stock.info.get('trailingPE', 'N/A')}")
        st.write(f"**Дивидендная доходность:** {stock.info.get('dividendYield', 'N/A')}")
        st.write(f"**Доходы:** {stock.info.get('totalRevenue', 'N/A')}")
        st.write(f"**Чистая прибыль:** {stock.info.get('netIncomeToCommon', 'N/A')}")

        # График цен акций
        st.header("График цен акций")
        hist = stock.history(period="1y")
        st.line_chart(hist["Close"], use_container_width=True)

        # Финансовые отчеты
        st.header("Финансовые отчеты")
        st.subheader("Отчет о доходах")
        st.write(stock.financials if not stock.financials.empty else "Данные недоступны")

        st.subheader("Балансовый отчет")
        st.write(stock.balance_sheet if not stock.balance_sheet.empty else "Данные недоступны")

        st.subheader("Отчет о движении денежных средств")
        st.write(stock.cashflow if not stock.cashflow.empty else "Данные недоступны")
        
    except Exception as e:
        st.error(f"Ошибка при загрузке данных: {e}")
