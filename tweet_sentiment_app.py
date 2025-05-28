import streamlit as st
import tweepy
from textblob import TextBlob
import pandas as pd

# Streamlit UI
st.set_page_config(page_title="Tweet Sentiment Analyzer", page_icon="🔍")
st.title("🔍 Live Tweet Sentiment Analyzer")

st.markdown("Analyze recent tweets in real-time based on a keyword or topic.")

# Get credentials and inputs
bearer_token = st.text_input("🔐 Enter your Twitter Bearer Token:", type="password")
query = st.text_input("🔎 Enter keyword to search tweets:", value="OpenAI")
count = st.slider("📊 Number of tweets to analyze:", min_value=5, max_value=50, value=10)

# Analyze button
if st.button("Analyze Sentiment"):
    if not bearer_token or not query:
        st.warning("Please enter your Twitter Bearer Token and search keyword.")
    else:
        try:
            # Twitter API setup
            client = tweepy.Client(bearer_token=bearer_token)

            # Fetch tweets
            with st.spinner("Fetching tweets..."):
                tweets = client.search_recent_tweets(query=query, max_results=count, tweet_fields=['text', 'created_at'])

            if not tweets.data:
                st.warning("No tweets found for this keyword.")
            else:
                # Analyze sentiment
                data = []
                for tweet in tweets.data:
                    text = tweet.text
                    blob = TextBlob(text)
                    sentiment = blob.sentiment.polarity
                    label = "Positive" if sentiment > 0 else "Negative" if sentiment < 0 else "Neutral"
                    data.append({
                        'Tweet': text,
                        'Sentiment Score': sentiment,
                        'Sentiment': label,
                        'Time': tweet.created_at
                    })
                
                df = pd.DataFrame(data)
                st.success(f"Analyzed {len(df)} tweets.")
                st.dataframe(df)

                st.markdown("### 📈 Sentiment Distribution")
                st.bar_chart(df['Sentiment'].value_counts())
        
        except Exception as e:
            st.error(f"Error: {e}")
