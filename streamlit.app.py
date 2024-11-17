import streamlit as st

# Titles
st.markdown("<h1 style='text-align: center;'>Investment and Machine Learning 2024</h1>", unsafe_allow_html=True)

# Main Content with full-width styling
st.markdown(
    """
    <style>
    .full-width-text {
        width: 100%;
        margin: 0;
        padding: 0;
        text-align: justify;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="full-width-text">
    Welcome to the Stock Analysis Application! This tool empowers investors by leveraging both Technical and Fundamental analysis approaches to evaluate stocks effectively.
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

    ### Why Use This Tool?
    This application helps you:
    - Identify trading opportunities with **technical analysis**.
    - Evaluate company performance for **long-term investments** using **fundamental analysis**.
    - Gain insights into market trends and patterns.

    Start your analysis by selecting the desired type of analysis and entering the stock ticker in the **sidebar**. Happy investing!
    </div>
    """,
    unsafe_allow_html=True
)
