import streamlit as st
import plotly.graph_objects as go

# Title for the Glossary Page
st.title("Glossary of Financial Terms")

# Introductory Text
st.markdown("""
This glossary provides definitions, examples, and interactive tools to enhance your understanding of financial and stock market concepts. 
Explore the terms below by category or search for a specific term.
""")

# Define Categories and Terms
categories = {
    "Valuation Metrics": {
        "P/E Ratio": {
            "definition": "The price-to-earnings (P/E) ratio is calculated by dividing a company's stock price by its earnings per share (EPS).",
            "example": "If a company's stock price is $50 and its EPS is $5, the P/E ratio is 10.",
            "formula": "P/E Ratio = Stock Price / EPS"
        },
        "Market Capitalization": {
            "definition": "The total value of a company's outstanding shares, calculated by multiplying the stock price by the number of shares.",
            "example": "If a company's stock price is $100 and it has 1 million shares, the market cap is $100 million.",
            "formula": "Market Cap = Stock Price × Number of Shares"
        }
    },
    "Technical Indicators": {
        "RSI": {
            "definition": "The Relative Strength Index (RSI) measures the speed and change of price movements on a scale of 0 to 100.",
            "example": "An RSI above 70 may indicate an overbought stock, while below 30 may indicate oversold conditions.",
            "formula": "RSI = 100 - [100 / (1 + RS)] (where RS = Average Gain / Average Loss)"
        },
        "Moving Average": {
            "definition": "A moving average smooths out price data to identify trends over a specific time frame.",
            "example": "A 50-day moving average shows the average closing price over the last 50 days.",
            "formula": "Moving Average = Sum of Closing Prices over N Days / N"
        }
    }
}

# Search Bar
search_term = st.text_input("Search for a term:")

# Filter by Category
selected_category = st.selectbox("Filter by Category", ["All"] + list(categories.keys()))

# Filtered Terms
filtered_terms = {}

if search_term:
    # Search across all categories
    for category, terms in categories.items():
        for term, details in terms.items():
            if search_term.lower() in term.lower():
                filtered_terms[term] = details
else:
    # Show terms from the selected category or all
    for category, terms in categories.items():
        if selected_category == "All" or selected_category == category:
            filtered_terms.update(terms)

# Display Terms
if not filtered_terms:
    st.warning("No terms found. Try searching for another term or select a different category.")
else:
    for term, details in filtered_terms.items():
        with st.expander(term):
            st.markdown(f"**Definition:** {details['definition']}")
            st.markdown(f"**Example:** {details['example']}")
            st.markdown(f"**Formula:** `{details['formula']}`")

# Example Visualization for RSI
if "RSI" in filtered_terms:
    st.subheader("Example RSI Chart")
    rsi_values = [30, 50, 70, 90]
    prices = [100, 110, 120, 130]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=rsi_values, y=prices, mode="lines+markers", name="Stock Price vs RSI"))
    fig.update_layout(title="Example RSI Chart", xaxis_title="RSI", yaxis_title="Stock Price", template="plotly_white")
    st.plotly_chart(fig)
