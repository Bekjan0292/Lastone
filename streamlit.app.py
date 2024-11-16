import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

# Set up page configuration
st.set_page_config(
    page_title="Stock Analyzer",
    page_icon="📈",
    layout="wide"
)

# Initialize session state to store the ticker
if "ticker" not in st.session_state:
    st.session_state["ticker"] = ""

# Define pages
def starting_page():
    st.title("Stock Analyzer")
    st.write("Welcome! This app allows you to analyze stocks both **fundamentally** and **technically**.")
    
    # Input ticker
    ticker = st.text_input("Enter Stock Ticker (e.g., AAPL, TSLA):", value=st.session_state["ticker"])
    st.session_state["ticker"] = ticker

    # Buttons for navigation
    if st.button("Go to Fundamental Analysis"):
        st.session_state["page"] = "Fundamental"
    if st.button("Go to Technical Analysis"):
        st.session_state["page"] = "Technical"

def fundamental_analysis():
    st.title("Fundamental Analysis")

    if "ticker" not in st.session_state or not st.session_state["ticker"]:
        st.warning("Please go back to the starting page and enter a stock ticker.")
    else:
        ticker = st.session_state["ticker"]
        stock = yf.Ticker(ticker)
        info = stock.info

        st.subheader(f"{info.get('longName', 'Unknown Company')} ({ticker})")

        st.markdown(f"""
        **Sector**: {info.get('sector', 'N/A')}  
        **Industry**: {info.get('industry', 'N/A')}  
        **Market Cap**: ${info.get('marketCap', 0):,}  
        **PE Ratio (TTM)**: {info.get('forwardPE', 'N/A')}  
        **Dividend Yield**: {info.get('dividendYield', 0) * 100:.2f}%  
        **52-Week High**: ${info.get('fiftyTwoWeekHigh', 'N/A')}  
        **52-Week Low**: ${info.get('fiftyTwoWeekLow', 'N/A')}  
        """)

    if st.button("Back to Start"):
        st.session_state["page"] = "Start"

def technical_analysis():
    st.title("Technical Analysis")

    if "ticker" not in st.session_state or not st.session_state["ticker"]:
        st.warning("Please go back to the starting page and enter a stock ticker.")
    else:
        ticker = st.session_state["ticker"]
        stock = yf.Ticker(ticker)
        history = stock.history(period="1y")

        # Price chart
        st.subheader("Price Chart (Last 1 Year)")
        fig = go.Figure()
        fig.add_trace(go.Candlestick(
            x=history.index,
            open=history['Open'],
            high=history['High'],
            low=history['Low'],
            close=history['Close'],
            name="Price"
        ))
        fig.update_layout(
            title="Price Chart",
            xaxis_title="Date",
            yaxis_title="Price",
            xaxis_rangeslider_visible=False
        )
        st.plotly_chart(fig)

        # Moving averages
        st.subheader("Moving Averages")
        history['SMA_50'] = history['Close'].rolling(window=50).mean()
        history['SMA_200'] = history['Close'].rolling(window=200).mean()
        st.line_chart(history[['Close', 'SMA_50', 'SMA_200']])

    if st.button("Back to Start"):
        st.session_state["page"] = "Start"

# Navigation logic
if "page" not in st.session_state:
    st.session_state["page"] = "Start"

if st.session_state["page"] == "Start":
    starting_page()
elif st.session_state["page"] == "Fundamental":
    fundamental_analysis()
elif st.session_state["page"] == "Technical":
    technical_analysis()
