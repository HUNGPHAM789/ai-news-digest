import os
import requests
import streamlit as st
from dotenv import load_dotenv

# Load API keys
load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
UNSPLASH_KEY = os.getenv("UNSPLASH_ACCESS_KEY")

# Define topics
topics = {
    "Nutrition": "nutrition",
    "World News": "world",
    "IELTS": "ielts",
    "Weather": "weather",
    "AI Development": "artificial intelligence"
}

# Function to fetch news from News API
def fetch_news(topic):
    url = f"https://newsapi.org/v2/everything?q={topic}&apiKey={NEWS_API_KEY}&pageSize=3"
    response = requests.get(url)
    if response.status_code != 200:
        return []
    return response.json().get("articles", [])

# Function to fetch image from Unsplash
def fetch_image(query):
    url = f"https://api.unsplash.com/photos/random?query={query}&client_id={UNSPLASH_KEY}"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    data = response.json()
    return data.get("urls", {}).get("small")

# Streamlit UI
st.set_page_config(page_title="News Digest", layout="wide")
st.title("📰 AI-Powered News Digest (No Summary)")

# Style
st.markdown("""
<style>
.card {
    background-color: #f9f9f9;
    padding: 1rem;
    border-radius: 10px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    margin-bottom: 1rem;
}
img {
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

# Display cards by category
for category, query in topics.items():
    st.header(category)
    articles = fetch_news(query)
    if not articles:
        st.write("No articles found.")
        continue
    cols = st.columns(3)
    for i, article in enumerate(articles):
        with cols[i % 3]:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            image_url = fetch_image(query)
            if image_url:
                st.image(image_url, use_column_width=True)
            st.markdown(f"**[{article.get('title', 'No Title')}]({article.get('url')})**", unsafe_allow_html=True)
            st.caption(article.get('source', {}).get('name', 'Unknown Source'))
            st.markdown('</div>', unsafe_allow_html=True)
