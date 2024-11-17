import streamlit as st

# Set up query parameters for navigation
query_params = st.experimental_get_query_params()

# Determine the section to display based on query parameter
section = query_params.get("section", ["Home"])[0]

# Sidebar Navigation
st.sidebar.title("Navigation")
st.sidebar.markdown(
    """
    - [Home](?section=Home)
    - [Technical Analysis](?section=Technical)
    - [Fundamental Analysis](?section=Fundamental)
    """
)

# Main Content
if section == "Home":
    st.title("Investment and Machine Learning, 2024")
    st.header("Stock Analysis")

    st.markdown("""
    Welcome to the **Stock Analysis Application**! This tool empowers investors by leveraging both **technical** and **fundamental analysis** approaches to evaluate stocks effectively.

    ### Types of Analysis and Investment Purposes:

    - **[Technical Analysis](?section=Technical)**:
      Focuses on short-term trading strategies like day trading and swing trading.
    - **[Fundamental Analysis](?section=Fundamental)**:
      Ideal for long-term investment strategies based on company growth and financial health.

    Click on the links above to learn more about each type of analysis!
    """)

elif section == "Technical":
    st.title("Technical Analysis")
    st.markdown("""
    ### What is Technical Analysis?
    - Focuses on historical price charts, trends, and patterns.
    - Tools include:
        - Moving averages
        - RSI (Relative Strength Index)
        - MACD (Moving Average Convergence Divergence)

    **Purpose**: Best suited for **short-term trading** strategies, such as:
    - Day trading
    - Swing trading
    """)

elif section == "Fundamental":
    st.title("Fundamental Analysis")
    st.markdown("""
    ### What is Fundamental Analysis?
    - Focuses on evaluating a company's financial health and growth potential.
    - Tools include:
        - Balance sheets
        - Income statements
        - Valuation metrics (P/E ratio, ROE, etc.)

    **Purpose**: Best suited for **long-term investments** aiming for:
    - Capital appreciation
    - Dividends
    """)
