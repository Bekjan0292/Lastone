import streamlit as st
from textblob import TextBlob
import requests

# Function to fetch news articles
def fetch_news(company_name):
    api_key = "a569f66a6b1a44348a05e18388610384"  # Replace with your News API key
    url = f"https://newsapi.org/v2/everything?q={company_name}&language=en&pageSize=5&apiKey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        articles = response.json().get("articles", [])
        return [{"title": article["title"], "url": article["url"]} for article in articles]
    else:
        st.error("Failed to fetch news. Please check your API key or try again later.")
        return []

# Function to perform sentiment analysis
def analyze_sentiment(headlines):
    sentiments = []
    for headline in headlines:
        blob = TextBlob(headline)
        polarity = blob.sentiment.polarity
        sentiments.append(polarity)
    overall_sentiment = sum(sentiments) / len(sentiments) if sentiments else 0
    return overall_sentiment

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
            for article in news:
                st.markdown(f"- [{article['title']}]({article['url']})")
            
            # Perform sentiment analysis
            headlines = [article["title"] for article in news]
            overall_sentiment = analyze_sentiment(headlines)
            
            # Display sentiment result
            st.subheader("Sentiment Analysis Result")
            if overall_sentiment > 0:
                st.success(f"Overall Sentiment: Positive ({overall_sentiment:.2f})")
            elif overall_sentiment < 0:
                st.error(f"Overall Sentiment: Negative ({overall_sentiment:.2f})")
            else:
                st.info("Overall Sentiment: Neutral (0.00)")
    else:
        st.warning("Please enter a company name.")
