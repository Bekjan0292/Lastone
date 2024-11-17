import streamlit as st
import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Initialize Sentiment Analyzer
analyzer = SentimentIntensityAnalyzer()

# Function to fetch news articles
def fetch_news(company_name):
    api_key = "a569f66a6b1a44348a05e18388610384"
    url = f"https://newsapi.org/v2/everything?q={company_name}&language=en&pageSize=5&apiKey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        articles = response.json().get("articles", [])
        return [{"title": article["title"], "url": article["url"]} for article in articles]
    else:
        st.error("Failed to fetch news. Please check your API key or try again later.")
        return []

# Function to analyze sentiment
def analyze_sentiment(headlines):
    results = []
    for headline in headlines:
        sentiment = analyzer.polarity_scores(headline)
        compound = sentiment['compound']
        if compound > 0:
            sentiment_type = "Positive"
        elif compound < 0:
            sentiment_type = "Negative"
        else:
            sentiment_type = "Neutral"
        results.append({"headline": headline, "sentiment": sentiment_type, "compound": compound})
    return results

# Streamlit page setup
st.title("Company Sentiment Analysis")
st.markdown("""
Enter the name of a company to fetch the latest news and perform sentiment analysis on the headlines.
""")

# User input
company_name = st.text_input("Enter Company Name:")

if st.button("Analyze Sentiment"):
    if company_name:
        # Fetch news articles
        news = fetch_news(company_name)
        
        if news:
            st.subheader(f"Latest News Headlines for {company_name}")
            headlines = []
            for i, article in enumerate(news, 1):
                st.markdown(f"{i}. [{article['title']}]({article['url']})")
                headlines.append(article["title"])
            
            # Perform sentiment analysis
            sentiment_results = analyze_sentiment(headlines)
            
            # Display sentiment results
            st.subheader("Sentiment Analysis Results")
            for result in sentiment_results:
                st.markdown(f"- **Headline**: {result['headline']}")
                st.markdown(f"  - Sentiment: **{result['sentiment']}**")
                st.markdown(f"  - Compound Score: {result['compound']:.2f}")
    else:
        st.warning("Please enter a company name.")
