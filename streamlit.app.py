import streamlit as st

# Titles
st.title("Investment and Machine Learning, 2024")
st.header("Stock Analysis")

# Main Content
st.markdown("""
Welcome to the **Stock Analysis Application**! This tool empowers investors by leveraging both **technical** and **fundamental analysis** approaches to evaluate stocks effectively.

---

### Types of Analysis and Investment Purposes:

#### **1. [Technical Analysis](Pages/2_Technical_Analysis)**
- **Purpose**: Ideal for **short-term trading** such as day trading and swing trading.
- **Focus**: 
    - Historical price movements, trends, and patterns.
    - Tools: Moving averages, RSI, MACD, candlestick charts.

#### **2. [Fundamental Analysis](Pages/1_Fundamental_Analysis)**
- **Purpose**: Designed for **long-term investment** strategies focusing on company growth and sustainability.
- **Focus**:
    - Financial health: Revenue, earnings, and balance sheets.
    - Valuation metrics: P/E ratio, ROE, and other key financial indicators.

---

### Why Use This Tool?
This application helps you:
- Identify trading opportunities with **technical analysis**.
- Evaluate company performance for **long-term investments** using **fundamental analysis**.
- Gain insights into market trends and patterns.

Use the links above or the sidebar navigation to explore the analysis tools. Happy investing!
""")
