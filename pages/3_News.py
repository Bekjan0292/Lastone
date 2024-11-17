import streamlit as st
import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd

# Initialize Sentiment Analyzer
analyzer = SentimentIntensityAnalyzer()

# Function to fetch news articles
def fetch_news(company_name):
    api_key = "YOUR_NEWS_API_KEY"  # Replace with your News API key
    url = f"https://newsapi.org/v2/everything?q={company_name}&language=en&pageSize=20&apiKey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        articles = response.json().get("articles", [])
        return [article["title"] for article in articles]
    else:
        st.error("Failed to fetch news. Please check your API key or try again later.")
        return []

# Function to analyze sentiment
def analyze_sentiment(headlines):
    results = []
    for headline in headlines:
        sentiment = analyzer.polarity_scores(headline)
        compound = sentiment['compound']
        results.append({"headline": headline, "compound": compound})
    return results

# Streamlit page setup
st.title("Company Sentiment Analysis")

# Short Info About Sentiment Analysis
st.markdown("""
**What is Sentiment Analysis?**  
Sentiment Analysis is a natural language processing (NLP) technique used to determine whether a piece of text has a positive, negative, or neutral sentiment.  
This tool analyzes the sentiment of the latest news headlines about a company to provide insights into market perception.
""")

# User input
company_name = st.text_input("Enter Company Name:")

if st.button("Analyze Sentiment"):
    if company_name:
        # Fetch news articles
        news = fetch_news(company_name)
        
        if news:
            # Filter news to exclude "removed" headlines
            valid_news = [headline for headline in news if "removed" not in headline.lower()]
            valid_news = valid_news[:10]  # Limit to 10 valid articles
            
            if valid_news:
                st.subheader(f"Latest News and Sentiment for {company_name}")

                # Analyze sentiment
                sentiment_results = analyze_sentiment(valid_news)

                # Prepare DataFrame for display
                data = {
                    "Latest News": [result["headline"] for result in sentiment_results],
                    "Compound Score": [result["compound"] for result in sentiment_results]
                }
                df = pd.DataFrame(data)

                # Display table
                st.table(df)

                # Display overall sentiment
                avg_sentiment = df["Compound Score"].mean()
                st.subheader("Overall Sentiment")
                if avg_sentiment > 0:
                    st.success(f"Overall Sentiment: Positive ({avg_sentiment:.2f})")
                elif avg_sentiment < 0:
                    st.error(f"Overall Sentiment: Negative ({avg_sentiment:.2f})")
                else:
                    st.info("Overall Sentiment: Neutral (0.00)")
            else:
                st.warning("No valid news headlines found.")
    else:
        st.warning("Please enter a company name.")
