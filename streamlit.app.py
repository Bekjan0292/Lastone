import streamlit as st

st.set_page_config(
    page_title="Stock Analyzer",
    page_icon="📈",
    layout="wide",
)

st.title("Welcome to the Stock Analyzer")
st.markdown(
    """
    This app allows you to analyze stocks both **fundamentally** and **technically**.  
    Use the sidebar to navigate between pages.
    """
)
