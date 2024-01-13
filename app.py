import streamlit as st
import requests
from datetime import datetime, timedelta

# Function to fetch news from News API
def get_news(api_key, query, from_date, to_date, country="in"):
    base_url = "https://newsapi.org/v2/everything"
    params = {
        "apiKey": api_key,
        "q": query,
        "from": from_date,
        "to": to_date,
        "language": "en",
        "sortBy": "popularity",
        "country": country,
    }
    response = requests.get(base_url, params=params)
    return response.json()

# Function to perform sentiment analysis
def analyze_sentiment(text):
    # Add your sentiment analysis logic here (using NLP libraries, models, etc.)
    # This could be a simple positive/negative sentiment analysis for demonstration purposes.
    # You might want to use a more sophisticated model for a real-world scenario.
    return "Positive" if "good" in text.lower() else "Negative"

# Streamlit App
st.title("Indian Economic and Financial News Sentiment Analysis")

# Sidebar for user input
st.sidebar.header("Options")
time_horizon = st.sidebar.selectbox("Select Time Horizon", ["1 week", "2 weeks", "1 month", "6 months"])

# Set the date range based on the selected time horizon
end_date = datetime.now()
if time_horizon == "1 week":
    start_date = end_date - timedelta(days=7)
elif time_horizon == "2 weeks":
    start_date = end_date - timedelta(days=14)
elif time_horizon == "1 month":
    start_date = end_date - timedelta(days=30)
elif time_horizon == "6 months":
    start_date = end_date - timedelta(days=180)

# API Key for News API (replace with your own key)
news_api_key = "5843e8b1715a4c1fb6628befb47ca1e8"

# Fetch news data
query = "(finance OR economic OR business) AND (India OR Indian)"
news_data = get_news(news_api_key, query, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))

# List to store trending topics and their scores
trending_topics = []

# Display news headlines and sentiment analysis
st.subheader(f"Indian Economic and Financial News Headlines for {time_horizon} ({start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')})")

for article in news_data.get("articles", []):
    title = article.get("title", "")
    description = article.get("description", "")
    
    # Skip articles without titles or descriptions
    if not title or not description:
        continue
    
    # Append topic and sentiment to the list
    topic = f"{title}. {description}"
    sentiment = analyze_sentiment(topic)
    trending_topics.append({"Topic": topic, "Sentiment": sentiment})

    st.write(f"**Title:** {title}")
    st.write(f"**Description:** {description}")
    st.write(f"**Sentiment:** {sentiment}")
    st.write("---")

# Display a table of trending topics at the end
st.subheader("Trending Topics with Scores")
st.table(trending_topics)
