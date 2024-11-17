import streamlit as st

# Set background image using custom HTML
page_bg_img = '''
<style>
body {
    background-image: url("https://www.financial-planning.com/images/financial-planning-concept-stock-analysis-machine-learning.jpg");
    background-size: cover;
    background-attachment: fixed;
    color: white;
}
div.stMarkdown {
    background-color: rgba(0, 0, 0, 0.7);
    padding: 15px;
    border-radius: 10px;
}
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)

# Titles
st.title("Investment and Machine Learning, 2024")
st.header("Stock Analysis")

# Main Text with explanations
st.markdown("""
Welcome to the **Stock Analysis Application**! This tool empowers investors by analyzing stocks with **technical** and **fundamental approaches**. It helps you make informed investment decisions.

### Types of Analysis and Their Investment Purposes:

1. **Technical Analysis**
   - Focus: Examines historical price movements, trends, and patterns.
   - Tools: Moving averages, RSI, MACD, and candlestick patterns.
   - **Purpose**: Ideal for short-term trading (e.g., day trading, swing trading).

2. **Fundamental Analysis**
   - Focus: Evaluates the financial health of a company, including revenue, earnings, and valuation metrics.
   - Tools: Financial ratios, balance sheets, income statements, and company news.
   - **Purpose**: Suitable for long-term investing, focusing on business growth and sustainability.

This application allows you to analyze stocks for both **short-term trading** and **long-term investment goals**. Select your preferred analysis type and proceed with your stock research!
""")
