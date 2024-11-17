import streamlit as st
import webbrowser

# Titles
st.title("Investment and Machine Learning, 2024")
st.header("Stock Analysis")

# Main Content
st.markdown("""
Welcome to the **Stock Analysis Application**! This tool empowers investors by leveraging both **technical** and **fundamental analysis** approaches to evaluate stocks effectively.

---

### Types of Analysis and Investment Purposes:

#### **Technical Analysis**
- **Purpose**: Ideal for **short-term trading** such as day trading and swing trading.
- **Focus**: 
    - Historical price movements, trends, and patterns.
    - Tools: Moving averages, RSI, MACD, candlestick charts.

#### **Fundamental Analysis**
- **Purpose**: Designed for **long-term investment** strategies focusing on company growth and sustainability.
- **Focus**:
    - Financial health: Revenue, earnings, and balance sheets.
    - Valuation metrics: P/E ratio, ROE, and other key financial indicators.

---

### Explore the Tools:
""")

# Buttons for Navigation
col1, col2 = st.columns(2)

with col1:
    if st.button("Go to Fundamental Analysis"):
        webbrowser.open("Pages/1_Fundamental_Analysis")  # Adjust URL for actual deployment

with col2:
    if st.button("Go to Technical Analysis"):
        webbrowser.open("Pages/2_Technical_Analysis")  # Adjust URL for actual deployment
